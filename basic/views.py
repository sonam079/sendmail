import time
from basic.helper import open_file, write_in_file, get_addr
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
import os
import re
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from basic.forms import EmailSubscriberAddForm, EmailTemplatesUploadForm
from basic.models import EmailTemplates, SubscribedEmail, SaveImageFromTemplates, SendEmail
from django.contrib import messages
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor
from bs4 import BeautifulSoup
from django.conf import settings
from urllib.request import urlopen as uReq
from selenium import webdriver

i = 0
args = []

pattern = re.compile(r"(.*).setOption\((.*)\);")  # Search for the .setoption() function --> echart.js
# Search for the new Chart() function --> chart.js
pattern1 = re.compile(r"var (.*) = new Chart\((.*),(.*)\)", re.MULTILINE | re.DOTALL)
# Search for the location where script file is making charts in echart.js
pattern2 = re.compile(
    r"echarts.init\(document.getElementById\((.*)\)\)|echarts.init\(document.getElementsByClassName\((.*)\)\)"
)


# Create your views here.
# For Home Page
def home(request):
    # Fetch templates from the Email_templates database
    emailTemplates = EmailTemplates.objects.all()
    # For Subscribe mail functionality
    if request.method == "POST":
        add_form = EmailSubscriberAddForm(request.POST or None)
        if add_form.is_valid():
            # print("Form is valid")
            instance = add_form.save(commit=False)
            # print("b")
            instance.save()
            # print("a")
            # messages.success(request, 'You have been subscribed')
            return redirect('basic:home')
        else:
            add_form = EmailSubscriberAddForm(request.POST or None)
    else:
        add_form = EmailSubscriberAddForm()

    context = {
        'add_form': add_form,
        'email_templates': emailTemplates,
        'errors': add_form.errors,
    }
    # print("Request User", request.user)
    return render(request, 'basic/index.html', context)


# Function for uploading the templates
@login_required
def uploadTemplates(request):
    # For uploading templates
    if request.method == "POST":
        add_form = EmailTemplatesUploadForm(request.POST, request.FILES)
        # print(os.access(str(request.FILES['templates']), os.W_OK))
        if add_form.is_valid():
            print("Form is valid")
            instance = add_form.save(commit=False)
            # print("a", type(instance))
            instance.templates_owner = request.user
            # print("b", instance)
            instance.save()
            # print(instance.pk)
            # Commented for testing purpose
            parse_template(instance.pk)
            #  To fetch charts and convert them into images
            return redirect('basic:home')
        else:
            print("Form is not valid")
            add_form = EmailTemplatesUploadForm(request.POST, request.FILES)
    else:
        print("asd")
        add_form = EmailTemplatesUploadForm()
    context = {'upload_form': add_form}
    return render(request, 'basic/upload_templates.html', context)


# Function for parsing templates and downloading the image from it
def parse_template(pk):
    checkparse = SaveImageFromTemplates.objects.all().filter(parentTemplates_id=pk)
    if checkparse:
        print("Already")
    else:
        # To check for different chart scripts and appending the image conversion script
        print("create")
        append_template(pk)
        emailTemplates = get_object_or_404(EmailTemplates, id=pk)
        template_name = emailTemplates
        # Open browser and get data
        browser = webdriver.Firefox()
        site = 'http://127.0.0.1:8000/media/' + str(template_name)
        browser.get(site)
        time.sleep(10)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        # To parse for all image tags and fetch their image sources
        id_pattern = re.compile(r"url[0-9]{1,6}")
        img_tags = soup.find_all(id=id_pattern)
        # print("img", img_tags)
        urls = [img['src'] for img in img_tags]

        ik = 0

        Directory = settings.MEDIA_ROOT
        os.chdir(Directory)
        for contains in urls:
            # Storing the fetched image in the media folder
            # print("Reached inside loop")
            imageName = str(template_name) + "_" + str(ik)

            ImageFile = open(imageName + '.jpeg', 'wb')
            ImageFile.write(uReq(contains).read())
            ImageFile.close()
            # Creating an instance of the stored image and saving it
            instance = SaveImageFromTemplates()
            instance.parentTemplates = emailTemplates
            instance.imageSource = 'http://127.0.0.1:8000/media/' + str(imageName) + str('.jpeg')
            instance.save()
            ik = ik + 1
        browser.quit()
        # For removing all the script and unwanted tags
        parse_and_append_templates(pk)
        # Send Templates
        # send_template(pk)

    # To append the script to add img tag and and to convert chart to image


def append_template(pk):
    print("append")
    # open the file which is uploaded now
    # Calls helper function to open the concerned file
    testFile = open_file(pk)
    # Using BeautifoulSoup for parsing
    soup = BeautifulSoup(testFile, "html.parser")
    # find all script file
    for script in soup.find_all('script'):
        script.text.replace('\n', '')
        # initiates slimit parser tree
        parser = Parser()
        # to parse through the script in html
        tree = parser.parse(script.text)

        for node in nodevisitor.visit(tree):
            # Calls function which appends image conversion code based on type of charts

            append_to_chart(node, soup, script)
            # Calls helper function to write the changed soup
            write_in_file(pk, soup)


# append the image at right place
def parse_and_append_templates(pk):
    global i
    # Calls helper function to open the concerned file
    testFile = open_file(pk)
    soup = BeautifulSoup(testFile, "html.parser")
    # Removing all the script tags
    [x.extract() for x in soup.find_all('script')]
    id_pattern = re.compile(r"url[0-9]{1,6}")
    # Removing all the image tags
    # [y.extract() for y in soup.find_all(id=id_pattern)]
    # Calls helper function to write the changed soup
    write_in_file(pk, soup)
    instance_image = SaveImageFromTemplates.objects.filter(parentTemplates_id=pk)
    k = 0

    imgs = soup.find_all('img', {'id': id_pattern})
    all_canvas = soup.find_all('canvas')
    if imgs and not all_canvas:
        for img_src, item in zip(instance_image, imgs):
            new_tag = soup.new_tag('img',
                                   src=img_src,
                                   id='url' + str(k))
            Div = item.previous_sibling.previous_sibling
            Div.append(new_tag)
            item.extract()
            write_in_file(pk, soup)
            k = k + 1

    else:
        [y.extract() for y in soup.find_all(id=id_pattern)]
        # Removing all the canvas in the Chart.js containing html
        for canvas, img_src in zip(all_canvas, instance_image):
            new_tag = soup.new_tag('img',
                                   src=img_src,
                                   id='url' + str(k),
                                   style="padding:15px; "
                                         "margin: 15px; "
                                         "align-self: center; "
                                         "display: inline-flex !important;")
            canvas.replaceWith(new_tag)
            write_in_file(pk, soup)
            k = k + 1

    i = 0


# For Sending mail as templates
def send_template(request, pk):
    subscribedEmail = SubscribedEmail.objects.values_list('email_address', flat=True)
    print(subscribedEmail)
    to = []
    to.append(subscribedEmail[0])
    for se in subscribedEmail:
        if se not in to:
            to.append(se)
    plaintext = get_template('basic/email.txt')
    # Calls helper function to get the address of the concerned file
    template_addr = get_addr(pk)
    htmly = get_template(template_addr)
    html_content = htmly.render()
    subject, from_email = 'Hello from vPhrase', 'evicharya@gmail.com'
    text_content = plaintext.render()
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
        templates = EmailTemplates.objects.filter(id=pk)
        num = templates.values_list('number_of_times_templates_send', flat=True)
        templates_owner = templates.values_list('templates_owner_id', flat=True)
        print("Num", num)
        user = User.objects.get(id=templates_owner[0])
        templates.update(number_of_times_templates_send=(int(num[0]) + 1))
        emailTemplates = get_object_or_404(EmailTemplates, id=pk)
        SendEmail.objects.create(template=emailTemplates, mail_send_user=user, number_of_mail=int(num[0]))
    except:
        print("Sorry there was some Problem")
    return render(request, 'basic/index.html')
    # return render(request, 'basic/email_sending_complete.html')


def append_to_chart(node, soup, script):
    global i
    # If the tree node is a Functional Call the html is compared with the regex
    if isinstance(node, ast.FunctionCall) and re.findall(pattern2, node.to_ecma()):
        for j in range(len(re.findall(pattern2, node.to_ecma()))):
            # Declared global as is to be used in parse_and_append function
            global args
            # For storing the ids of the tags in which charts are rendered
            arg3 = re.search(pattern2, node.to_ecma()).group(1)
            # Ids are then used to Place converted chart images at their resp. Divs in the html file.
            args.append(arg3.strip('\'\"'))
            print(args)
    # ------------------------For Chart.js-----------------------------------
    if isinstance(node, ast.VarStatement):
        # If the tree node is a Var Statement the html is compared with the regex
        if re.findall(pattern1, node.to_ecma()):
            new_tag = soup.new_tag('img', id='url' + str(i), src="", style="height:500px!important;")
            arg1 = re.search(pattern1, node.to_ecma()).group(1)
            soup.body.append(new_tag)

            # Script to convert chart.js to images appended
            script.append(
                " function updateConfigByMutating(" + arg1 + ") {\n\t" + arg1 +
                ".options.animation.onComplete = function done()"
                "{ var url = " + arg1 + ".toBase64Image();" "document.getElementById('url" + str(
                    i) + "').src= url};\n\t" + arg1 + ".update();\t}\n updateConfigByMutating(" + arg1 + ");")
            print("Append Here")
    # print("Appended in the Variable Statement")

    # ---------------------------------For echarts.js--------------------------------------------
    # Script to convert echarts.js to images appended
    if isinstance(node, ast.ExprStatement):

        if re.findall(pattern, node.to_ecma()):
            for item in args:
                div = soup.find('div', {'id': str(item)})
                new_tag = soup.new_tag('img', id='url' + str(i), src="")
                div.insert_after(new_tag)
                arg = re.match(pattern, node.to_ecma()).group(1)
                # Script to convert echarts.js to images appended
                script.append(" var img = document.getElementById('url" + str(
                    i) + "');img.src = " + arg + ".getDataURL({ pixelRatio: 1,backgroundColor: '#fff'});")
            args.clear()
        i = i + 1
    # print(soup.prettify())


def error400(request):
    return render(request, 'basic/error/HTTP400.html')


def error403(request):
    return render(request, 'basic/error/HTTP403.html')


def error404(request):
    return render(request, 'basic/error/HTTP404.html')


def error500(request):
    return render(request, 'basic/error/HTTP500.html')


def error200(request):
    return render(request, 'basic/error/HTTP500.html')
