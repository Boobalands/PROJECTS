from django.shortcuts import render, redirect
from . models import UserPersonalModel
from . forms import UserPersonalForm, UserRegisterForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
import numpy as np
import pandas as pd
import joblib

import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from django.contrib.auth.decorators import login_required

import base64
from io import BytesIO

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
        fieldss = ['firstname','lastname','age','address','phone','city','state','country']
        form = UserPersonalForm(request.POST)
        if form.is_valid():
            print('Saving data in Form')
            form.save()
        return render(request, '4_Home.html', {'form':form})
    else:
        print('Else working')
        form = UserPersonalForm(request.POST)    
        return render(request, '6_Per_Info.html', {'form':form})
    
def Per_Database_7(request):
    models = UserPersonalModel.objects.all()
    return render(request, '7_Per_Database.html', {'models':models})


a = joblib.load('C:/Users/SPIRO-PYTHON/Desktop/PROJECTS/TIME_SERIES_FORCASTING/PROJECT/APP/RFC.pkl')  
@login_required(login_url='Login_3')
def Deploy_8(request): 
    if request.method == "POST":
        int_features = [x for x in request.POST.values()]
        int_features = int_features[1:]
        print(int_features)
        final_features = [np.array(int_features, dtype=object)]
        print(final_features)
        prediction = a.predict(final_features)
        print(prediction)
        output = prediction[0]
        print(output)

        return render(request, '8_Deploy.html', {"prediction_text":f'THE BANK CLIENT FIDELITY IS {output} %'})
    else:
        return render(request, '8_Deploy.html')
    
    
@login_required(login_url='Login_3')
def Deploy_9(request): 
    if request.method == "POST":
        int_features = [x for x in request.POST.values()]
        int_features = int_features[1:]
        print(int_features)

        data = pd.read_csv("C:/Users/SPIRO-PYTHON/Desktop/PROJECTS/TIME_SERIES_FORCASTING/PROJECT/APP/attrition.csv")
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

        daily_data = data.resample('D').sum()

        train_size = int(0.8 * len(daily_data))
        train_data, test_data = daily_data.iloc[:train_size], daily_data.iloc[train_size:]

        smoothing_model = ExponentialSmoothing(train_data, seasonal='add', seasonal_periods=70)
        fit_model = smoothing_model.fit()

        forecast_start = pd.to_datetime(int_features[0])
        forecast_end = pd.to_datetime(int_features[1])
        forecast_index = pd.date_range(start=forecast_start, end=forecast_end, freq='D')

        forecast_steps = len(forecast_index)
        forecast_values = fit_model.forecast(steps=forecast_steps)

        forecast_df = pd.DataFrame({'Date': forecast_index, 'Forecasted_Sales': forecast_values})
        forecast_df.set_index('Date', inplace=True)  
        print(forecast_df)

        forecast_df.to_csv("FILES/EXPONENTIAL.csv", index=True)

        img_bytes = BytesIO()
        plt.figure(figsize=(12, 6))
        plt.plot(daily_data.index, daily_data['Sales'], color='blue', linestyle='-', marker='o', label='Actual Sales')
        plt.plot(forecast_index, forecast_values, color='red', linestyle='--', marker='x', label='Forecasted Sales')
        plt.xlabel('Date')
        plt.ylabel('Sales')
        plt.title('Sales Forecasting using EXPONENTIAL SMOOTHING')
        plt.legend()
        plt.grid(True)  
        plt.savefig(img_bytes, format='png')
        plt.close()

        img_base64 = base64.b64encode(img_bytes.getvalue()).decode()

        return render(request, '9_Deploy.html', {"prediction_image": img_base64})

    else:
        return render(request, '9_Deploy.html')


@login_required(login_url='Login_3')
def Logout(request):
    logout(request)
    return redirect('Login_3')
