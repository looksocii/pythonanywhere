from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from django.core.files import File
import os, shutil
from Service_App.issue_credential import createCredentialManifest, zip_tool, issueCredential
from Service_App.select_credential.selectCredential import selectCredential
from Service_App.select_credential.credentialData import get_credential
from Service_App.verify_credential.verifyCredential import verifyCredential

SAVED_FILES_DIR = r'files'

@require_GET
def home(request):
    return render(request, 'home.html', {})

@require_POST
def issue_credential(request):
    file = request.FILES.get("issueCredential", None)
    if not file:
        return home(request)

    return issue(request, file)


def issue(request, file):
	extract_file_path = 'Service_App/issue_credential'
	if os.path.exists(extract_file_path + '/credential') and os.path.exists(extract_file_path + '/association'):
		shutil.rmtree(extract_file_path + '/credential')
		shutil.rmtree(extract_file_path + '/association')
	if os.path.isfile(extract_file_path + '/issuer.json'):
		os.remove(extract_file_path + '/issuer.json')
	if os.path.isfile(extract_file_path + '/issue_conf.json'):
		os.remove(extract_file_path + '/issue_conf.json')
	#extract receive zip file
	zip_tool.unzip_file(file, extract_file_path)

	createCredentialManifest.create()
	#issue credential
	tx_id, chain = issueCredential.issue()

	source_file = extract_file_path + '/data'
	issueFile_path = 'files/issueFile/data.zip'

	zip_tool.zip_file(source_file,issueFile_path)

	files = os.listdir(SAVED_FILES_DIR + '/issueFile')

	return render(request, 'issue.html', {'files': files, 'tx_id': tx_id})


def issuer(request):
	return render(request, 'issuer.json', {})


@require_GET
def download_issueFile(request, filename):
    file_pathname = os.path.join(SAVED_FILES_DIR + '/issueFile', filename)

    with open(file_pathname, 'rb') as f:
        file = File(f)

        response = HttpResponse(file.chunks(),
                                content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Length'] = os.path.getsize(file_pathname)

    return response


@require_POST
def upload_credential(request):
	file = request.FILES.get("selectCredential", None)
	extract_file_path = 'Service_App/select_credential/data'

	if os.path.isfile(extract_file_path + '/manifest.json'):
	    os.remove(extract_file_path + '/manifest.json')

	if os.path.exists(extract_file_path + '/credential'):
	    shutil.rmtree(extract_file_path + '/credential')

	#extract receive zip file
	zip_tool.unzip_file(file, extract_file_path)

	credential_list = get_credential()

	return render(request, 'select_credential.html', {'credential_list': credential_list})


@require_POST
def select_credential(request):
	file = request.FILES.get("selectCredential", None)

	return select(request, file)


def select(request, file):
	selectList = request.POST.getlist("selected_credential")
	selectCredential(selectList)

	source_file = 'Service_App/select_credential/select_data'
	selectFile_path = 'files/selectFile/select_data.zip'

	zip_tool.zip_file(source_file,selectFile_path)

	files = os.listdir(SAVED_FILES_DIR + '/selectFile')

	return render(request, 'select.html', {'files': files})

@require_GET
def download_selectFile(request, filename):
    file_pathname = os.path.join(SAVED_FILES_DIR + '/selectFile', filename)

    with open(file_pathname, 'rb') as f:
        file = File(f)

        response = HttpResponse(file.chunks(),
                                content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Length'] = os.path.getsize(file_pathname)

    return response


@require_POST
def verify_credential(request):
	file = request.FILES.get("verifyCredential", None)
	return verify(request, file)


def verify(request, file):
	extract_file_path = 'Service_App/verify_credential/data'

	if os.path.isfile(extract_file_path + '/credential.json'):
		os.remove(extract_file_path + '/credential.json')
	if os.path.isfile(extract_file_path + '/manifest.json'):
		os.remove(extract_file_path + '/manifest.json')

	#extract receive zip file
	zip_tool.unzip_file(file, extract_file_path)

	result_list = verifyCredential()

	return render(request, 'verify.html', {'result_list': result_list})

