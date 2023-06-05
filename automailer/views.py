
from mailer import settings
from .models import Transaction
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import UserLoginForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView



def home(request):
    return render(request, 'home.html')


@login_required
def profile_view(request):
    return render(request, "profile.html")



def create_transaction(request):
    t_amount = request.POST.get('amount')
    t_receiver = request.POST.get('receiver')
    t_currency = str(request.POST.get('currency')).upper()
    wallet = request.POST.get('wallet', '')  # Provide a default value if 'wallet' is not present
    transaction_details = Transaction.objects.create(amount=t_amount, reciever=t_receiver)
    transaction_details.save()
    return t_amount, t_currency, wallet




def send_confirmation_email(e_subject, receiver_email, t_amount, t_currency, wallet_ID,  e_template=''):
    email_context = {
        'amount': t_amount,
        't_currency': t_currency,
        'wallet':wallet_ID,
    }
    email_subject = e_subject
    email_body = render_to_string(e_template, context=email_context)
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[receiver_email],
        reply_to=[settings.EMAIL_HOST_USER]
    )
    email.content_subtype = "html"
    email.send()


def binance_deposit(request):
    context = {}
    if request.method == 'POST':
        t_amount, t_currency, wallet = create_transaction(request)
        transaction = Transaction.objects.last()
        if transaction:
            receiver_email = transaction.reciever
            if receiver_email:
                email_subject = f"[Binance] Deposit Confirmed - {timezone.now().strftime('%Y-%m-%d %H:%M:%S (UTC)')}"
                binance_template = 'email_templates/binance_deposit_temp.html'

                send_confirmation_email(email_subject, receiver_email, t_amount, t_currency, wallet, e_template=binance_template)

                messages.success(request, "Deposit successful!")
                return redirect('binance_deposit')
            else:
                # Handle the case when the receiver's email address is missing or invalid
                messages.error(request, "Invalid receiver's email address.")
        else:
            # Handle the case when no transaction is found
            messages.error(request, "No transaction found.")
    
    return render(request, 'binance_deposit_form.html', context)

def binance_withdrawal(request):
    context = {}
    if request.method == 'POST':
        t_amount, t_currency, wallet = create_transaction(request)
        transaction = Transaction.objects.last()
        if transaction:
            receiver_email = transaction.reciever
            if receiver_email:
                email_subject = f"[Binance] Deposit Confirmed - {timezone.now().strftime('%Y-%m-%d %H:%M:%S (UTC)')}"
                binance_template = 'email_templates/binance_withdrawal_temp.html'

                send_confirmation_email(email_subject, receiver_email, t_amount, t_currency, wallet, e_template=binance_template)

                messages.success(request, "Withdrawal successful!")
                return redirect('binance_withdrawal')
            else:
                # Handle the case when the receiver's email address is missing or invalid
                messages.error(request, "Invalid receiver's email address.")
        else:
            # Handle the case when no transaction is found
            messages.error(request, "No transaction found.")
    
    return render(request, 'binance_withdrawal_form.html', context)




def blockchain_withdrawal(request):
    context = {}
    if request.method == 'POST':
        t_amount, t_currency, wallet = create_transaction(request)
        transaction = Transaction.objects.last()
        if transaction:
            receiver_email = transaction.reciever
            if receiver_email:
                e_subject = 'Your funds have been sent'
                blockchain_template = 'email_templates/blockchain_withdrawal_temp.html'

                send_confirmation_email(e_subject, receiver_email, t_amount, t_currency, e_template=blockchain_template, wallet_ID=wallet)

                messages.success(request, "Withdrawal successful!")

                return redirect('blockchain_withdrawal')
            else:
                messages.error(request, "Invalid Email Address")
        else:
            messages.error(request, "No transactions Found")

    return render(request, 'blockchain_withdrawal_form.html', context)


'blockchain_recieve_form'
def blockchain_recieve(request):
    context = {}
    if request.method == 'POST':
        t_amount, t_currency, wallet = create_transaction(request)
        transaction = Transaction.objects.last().reciever
        if transaction:
            receiver_email =transaction
            if receiver_email:
                e_subject = "You've received funds in your Private Key Wallet"
                blockchain_template = 'email_templates/blockchain_recieve_temp.html'

                send_confirmation_email(e_subject, receiver_email, t_amount, t_currency, wallet, e_template=blockchain_template)

                messages.success(request, "Recieved successfully!")
                return redirect('blockchain_recieve')
            else:
                messages.error(request, "Invalid Receiver Email Addreess")
        else:
            messages.error(request, "No Transactoion Found")

    return render(request, 'blockchain_recieve_form.html', context)



def coinbase_send(request):
    context = {}
    if request.method == 'POST':
        t_amount = request.POST.get('amount')
        t_receiver = request.POST.get('receiver')
        t_currency = str(request.POST.get('currency')).upper()
        wallet = request.POST.get('wallet', '')  # Provide a default value if 'wallet' is not present
        transaction_details = Transaction.objects.create(amount=t_amount, reciever=t_receiver)
        transaction = Transaction.objects.last().reciever
        transaction_details.save()
        
        if transaction:
            receiver_email = transaction
            if receiver_email:
                e_subject = "You've received funds in your Private Key Wallet"
                blockchain_template = 'email_templates/coinbase_send_temp.html'

                send_confirmation_email(e_subject, receiver_email, t_amount, t_currency, wallet, e_template=blockchain_template)

                messages.success(request, "Crypto Sent successfully!")
                return redirect('coinbase_send')
            else:
                messages.error(request, "Invalid Receiver Email Addreess")
        else:
            messages.error(request, "No Transactoion Found")

    return render(request, 'coinbase_send_form.html', context)

#///////////////////////register PAGE////////////////////////////#
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'userforms/register.html', {'form': form})

#///////////////////////LOGIN PAGE////////////////////////////#
class UserLoginView(LoginView):
    template_name = 'userforms/login.html'
    form_class = UserLoginForm
    next_page = 'binance_deposit'

class UserLogoutView(LogoutView):
    template_name = 'userforms/login.html'
    next_page = 'home'
