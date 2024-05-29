from django.shortcuts import render
from .models import UserPredictModel
from .forms import UserPredictForm

from django.shortcuts import render, redirect
from . models import UserPersonalModel
from . forms import UserPersonalForm, UserRegisterForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import os
os.environ['HUGGINGFACEHUB_API_TOKEN']="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"


def Landing_1(request):
    return render(request, '1_Landing.html')

def Register_2(request):
    form = UserRegisterForm()
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was successfully created. ' + user)
            return redirect('Login_3')

    context = {'form':form}
    return render(request, '2_Register.html', context)

def Login_3(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home_4')
        else:
            messages.info(request, 'Username OR Password incorrect')

    context = {}
    return render(request,'3_Login.html', context)

@login_required(login_url='Login_3')
def Home_4(request):
    return render(request, '4_Home.html')

@login_required(login_url='Login_3')
def Teamates_5(request):
    return render(request,'5_Teamates.html')

@login_required(login_url='Login_3')
def Per_Info_6(request):
    
    if request.method == 'POST':
        print('Data is valid')
        form = UserPersonalForm(request.POST, request.FILES)
        if form.is_valid():
            print('Personal form is valid')
            form.save()
            return redirect('Home_4')
        else:
            return render(request, '6_Per_Info.html', {'form':form})
    else:
        form = UserPersonalForm()      
        return render(request, '6_Per_Info.html', {'form':form})


from langchain_huggingface import HuggingFaceEndpoint
repo_id="mistralai/Mistral-7B-Instruct-v0.2"
hf=HuggingFaceEndpoint(repo_id=repo_id,max_length=128,temperature=0.7)


from langchain import hub
prompt = hub.pull("rlm/rag-prompt") 


from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory
memory = ConversationBufferWindowMemory(k=1)


from langchain_community.embeddings import HuggingFaceBgeEmbeddings
huggingface_embeddings=HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",    
    model_kwargs={'device':'cpu'},
    encode_kwargs={'normalize_embeddings':True})


from langchain_community.document_loaders import WebBaseLoader
import bs4
loader=WebBaseLoader(web_paths=("https://en.wikipedia.org/wiki/India",),
                    bs_kwargs=dict(parse_only=bs4.SoupStrainer(
                        class_=("post-title","post-content","post-header")

                    )))
data = loader.load()


from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(data)


from langchain_objectbox.vectorstores import ObjectBox
vector = ObjectBox.from_documents(documents, huggingface_embeddings, embedding_dimensions=768)
vector

@login_required(login_url='Login_3')
def Per_Database_7(request):
    models = UserPersonalModel.objects.all()
    return render(request, '7_Per_Database.html', {'models':models})

@login_required(login_url='Login_3')
def Deploy_8(request):
    if request.method == 'POST':
        form = UserPredictForm(request.POST)

        if form.is_valid():
            form.save()
            user_input = form.cleaned_data.get('text')

            from langchain.chains import RetrievalQA
            qa_chain = RetrievalQA.from_chain_type(
                    llm=hf,
                    retriever=vector.as_retriever(),
                    chain_type_kwargs={"prompt": prompt},
                    memory=memory)
            
            result = qa_chain({"query": user_input })
            response = result['result']

            data = UserPredictModel.objects.latest('id')
            data.label = response
            data.save()
            models = UserPredictModel.objects.all()
            return render(request, '8_Deploy.html', {'form': form, 'models': models})

    else:
        print('Else working')
        form = UserPredictForm()
    models = UserPredictModel.objects.all()
    return render(request, '8_Deploy.html', {'form': form, 'models': models})

@login_required(login_url='Login_3')
def Logout(request):
    logout(request)
    return redirect('Login_3')

