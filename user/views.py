from django.shortcuts import render,redirect
from django.db.models import Avg, Count
from . models import *
def home(request):
    user_id = request.session.get('user_id')
    is_following_anyone = False

    if user_id:
        user = tblUser.objects.filter(userID=user_id).first()
        # User jo doctors ko follow karta hai unki list
        followed = tblFollow.objects.filter(userID=user).values_list('doctorID', flat=True)
        if followed.exists():
            is_following_anyone = True
            blogs = tblDoctorPost.objects.filter(doctorID__in=followed).order_by('-createDT')
        else:
            blogs = tblDoctorPost.objects.all().order_by('-createDT')
    else:
        blogs = tblDoctorPost.objects.all().order_by('-createDT')

    data = {
        'blogs': blogs,
        'is_following_anyone': is_following_anyone,
        'recent_posts':tblDoctorPost.objects.all().order_by('-createDT')[:5]
    }
    return render(request, 'home.html', data)
# Create your views here.

def Login(request):
    if request.POST.get('btnLogin'):
        email=request.POST.get('emailaddress')
        password=request.POST.get('password')
        u=tblUser.objects.filter(email=email,password=password).first()

        if u == None:
            data={"msg":"invalid credentials"}
            return render(request,'Login.html',data)
        elif not u.IsDoctor:
            c=tblClient.objects.filter(userID=u).first()
            if c:
                request.session['isDoctor']=False
                request.session['user_id']=u.userID
                request.session['user_name']=u.userName
                request.session['profilePic']=u.profilePic.url
                request.session['clientID']=c.clientID  
                return redirect(patientDashboard)
            else:
                data={"msg":"Client record not found"}
                return render(request,'Login.html',data)
        else:
            d=tblDoctor.objects.filter(userID=u).first()
            if d:
                request.session['isDoctor']=True
                request.session['user_id']=u.userID
                request.session['user_name']=u.userName
                request.session['profilePic']=u.profilePic.url
                request.session['doctorID']=d.doctorID
                request.session['displayName']=d.displayName
                # request.session['subcategory']=d.subcategoryID.subcategoryName
                return redirect(doctorDashboard)
            else:
                data={"msg":"Doctor record not found"}
                return render(request,'Login.html',data)

    return render(request,'Login.html')

def doctorRegister(request):
    data={
        'cities':tblCity.objects.all(),
        'subcategories':tblSubcategory.objects.all()
    }
    if request.POST.get('btnRegister'):
        name=request.POST.get('uname')
        password=request.POST.get('password')
        datetime=request.POST.get('dob')
        profile=request.FILES.get('profile')
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        city=request.POST.get('city')
        isDoctor= True
        u=tblUser.objects.filter(email=email).first()
        if u:
            data={"msg":"Email already exists"}
            return render(request,'doctor_register.html',data)
        else:
            user=tblUser(None,name,password,datetime,profile,email,contact,city,isDoctor)
            user.save()

            if isDoctor:
                isDoctor = True
                subcategory=request.POST.get('subcategory')
                bio=request.POST.get('bio')
                mode=request.POST.get('mode')
                dname=request.POST.get('displayName')
                dcontact=request.POST.get('displayContact')
                daddress=request.POST.get('displayAddress')
                d=tblDoctor(None,user.userID,dname,dcontact,bio,subcategory,daddress,mode)
                d.save()
                docImage=tblDoctorImages(None,d.doctorID,profile)
                docImage.save()
                return redirect(Login)
            else:
                isDoctor = False


        return redirect(Login)    
    return render(request,'doctor_register.html',data)

def doctorProfile(request):
    doctor_id=request.session['doctorID']
    blogs=tblDoctorPost.objects.filter(doctorID=doctor_id)
    blog_count=blogs.count()
    doctor = tblDoctor.objects.filter(doctorID=doctor_id).first()
    follower_count = tblFollow.objects.filter(doctorID=doctor).count() if doctor else 0
    review_count = tblReview.objects.filter(doctorID=doctor).count() if doctor else 0
    avg_rating_dict = tblReview.objects.filter(doctorID=doctor).aggregate(Avg('rating'))
    avg_rating = round(avg_rating_dict['rating__avg'] or 0.0, 1)
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES.get('image')
        tblDoctorImages.objects.create(doctorID=doctor, imageURL=image)
        return redirect(doctorProfile)

    doctor_images = tblDoctorImages.objects.filter(doctorID=doctor_id)
    data={
        "blogs":blogs,
        "blog_count":blog_count,
        "follower_count":follower_count,
        "review_count":review_count,
        "avg_rating":avg_rating,
        "doctor_images": doctor_images
    }
    return render(request,'doctor_profile.html',data)

def doctorPostDetails(request,id):
    data={
        "blogs":tblDoctorPost.objects.filter(doctorPostID=id),
        'comments':tblComments.objects.filter(doctorPostID=id, parent=None).order_by('-createdDT')
    }
    if request.POST.get('btnComment'):
        comment=request.POST.get('comment')
        parent_id=request.POST.get('parent_id')
        user_id=request.session['user_id']
        post=tblDoctorPost.objects.filter(doctorPostID=id).first()
        user=tblUser.objects.filter(userID=user_id).first()
        if user_id:
            parent_obj=None
            if parent_id:
                parent_obj=tblComments.objects.filter(commentsID=parent_id).first()
            new_comment=tblComments(
                comment=comment,
                userID=user,
                doctorPostID=post,
                parent=parent_obj
            )
            new_comment.save()
            return redirect('doctorPostDetails', id=id)
    return render(request,'doctor_post_details.html',data)

def doctorPostAdd(request):
    if request.POST.get('btnAddBlog'):
        title=request.POST.get('title')
        description=request.POST.get('description')
        profile=request.FILES.get('profile')
        
        user_id=request.session['user_id']
        if user_id:
            try:
                doctor=tblDoctor.objects.filter(userID=user_id).first()
                post=tblDoctorPost(None,doctor.doctorID,title,description,profile)
                post.save()
                return redirect('doctorPostDetails', id=post.doctorPostID)
            except:
                print("Doctor not found")
    data={
        'blogs':tblDoctorPost.objects.all()
    }
    return render(request,'doctor_post_add.html',data)

def patientRegister(request):
    data={
        'cities':tblCity.objects.all()
    }
    if request.POST.get('btnPRegister'):
        name=request.POST.get('uname')
        password=request.POST.get('password')
        profile=request.FILES.get('profile')
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        city=request.POST.get('city')
        isDoctor= False
        u=tblUser.objects.filter(email=email).first()
        if u:
            data={"msg":"Email already exists"}
            return render(request,'pateient_register.html',data)
        else:
            user=tblUser(None,name,password,datetime,profile,email,contact,city,isDoctor)
            user.save()

            if isDoctor == False:
                desc=request.POST.get('description')
                dob=request.POST.get('dob')
                gender=request.POST.get('gender')
                bloodGroup=request.POST.get('bloodGroup')
                patient=tblClient(None,user.userID,name,desc,dob,gender,bloodGroup)
                patient.save()
                return redirect(Login)
    return render(request,'pateient_register.html',data)

def logout(requset):
    requset.session.flush()
    return redirect(Login)

def doctorSearch(request):
    if 'user_id' not in request.session:
        return redirect('Login')
    
    query = request.POST.get('q', '') or request.GET.get('q', '')
    city_id = request.POST.get('city', '') or request.GET.get('city', '')
    subcategory_id = request.POST.get('subcategory', '') or request.GET.get('subcategory', '')
    rating_filter = request.POST.get('rating', '') or request.GET.get('rating', '')
    doctors = tblDoctor.objects.all()
    
    logged_in_user_id = request.session.get('user_id')
    if logged_in_user_id:
        logged_in_doctor = tblDoctor.objects.filter(userID=logged_in_user_id).first()
        if logged_in_doctor:
            doctors = doctors.exclude(doctorID=logged_in_doctor.doctorID)
            
    
    if query:
        doctors = doctors.filter(displayName__icontains=query)
    
    if city_id:
        doctors = doctors.filter(userID__cityID=city_id)
        
    if subcategory_id:
        doctors = doctors.filter(subcategoryID=subcategory_id)

    # Annotate doctors with their average rating
    doctors = doctors.annotate(avg_rating=Avg('tblreview__rating'))

    if rating_filter:
        try:
            rating_val = float(rating_filter)
            # Filter where avg_rating is not None AND >= rating_val
            doctors = doctors.filter(avg_rating__isnull=False, avg_rating__gte=rating_val)
        except ValueError:
            pass
    
    data = {
        'doctors': doctors,
        'query': query,
        'selected_city': city_id,
        'selected_cat': subcategory_id,
        'selected_rating': rating_filter,
        'cities': tblCity.objects.all(),
        'subcategories': tblSubcategory.objects.all()
    }
    return render(request, 'doctor_search.html', data)
def followDoctor(request, id):
    if 'user_id' not in request.session:
        return redirect('Login')

    user_id = request.session['user_id']
    user = tblUser.objects.filter(userID=user_id).first()
    doctor = tblDoctor.objects.filter(doctorID=id).first()

    if user and doctor:
        existing = tblFollow.objects.filter(userID=user, doctorID=doctor).first()
        if existing:
            existing.delete()   # Unfollow
        else:
            tblFollow.objects.create(userID=user, doctorID=doctor)  # Follow

    return redirect('viewDoctorProfile', id=id)

def viewDoctorProfile(request, id):
    user_id = request.session.get('user_id')
    doctor = tblDoctor.objects.filter(doctorID=id).first()
    
    # Check if user has already reviewed this doctor
    has_reviewed = False
    if user_id:
        has_reviewed = tblReview.objects.filter(doctorID=id, userID=user_id).exists()
    
    if request.POST.get('btnReview'):
        if not has_reviewed:
            review_text = request.POST.get('message')
            rating = request.POST.get('rating')
            r = tblReview(doctorID_id=id, userID_id=user_id, rating=rating, review=review_text)
            r.save()
            return redirect('viewDoctorProfile', id=id)
    
    rating=tblReview.objects.filter(doctorID=id, userID=user_id).first()
    
    # Calculate average rating
    avg_rating_dict = tblReview.objects.filter(doctorID=id).aggregate(Avg('rating'))
    avg_rating = avg_rating_dict['rating__avg'] or 0.0


    user_id = request.session['user_id']
    user = tblUser.objects.filter(userID=user_id).first()
    is_followed = False
    if user and doctor:
        is_followed = tblFollow.objects.filter(userID=user, doctorID=doctor).exists()

    follower_count = tblFollow.objects.filter(doctorID=doctor).count() if doctor else 0

    # Check if logged-in user is the doctor themselves
    is_own_profile = request.session.get('isDoctor') and request.session.get('doctorID') == id

    blogs = tblDoctorPost.objects.filter(doctorID=id)
    blog_count = blogs.count()

    reviews_qs = tblReview.objects.filter(doctorID=id).order_by('-createdDT')
    review_count = reviews_qs.count()

    doctor_images = tblDoctorImages.objects.filter(doctorID=id)
    data = {
        "doctor": doctor,
        "blogs": blogs,
        "reviews": reviews_qs,
        "is_followed": is_followed,
        "follower_count": follower_count,
        "is_own_profile": is_own_profile,
        "blog_count": blog_count,
        "has_reviewed": has_reviewed,
        "avg_rating": round(avg_rating, 1), # rounding to 1 decimal place
        "review_count": review_count,
        "doctor_images": doctor_images
    }

    return render(request, 'doctor_view_profile.html', data)

def doctorUpdateProfile(request):
    data={
        "doctor":tblDoctor.objects.filter(doctorID=request.session['doctorID']).first(),
        "cities":tblCity.objects.all(),
        "subcategories":tblSubcategory.objects.all(),
        "user":tblUser.objects.filter(userID=request.session['user_id']).first()   
    }
    doctor_id=request.session['doctorID']
    user_id=request.session['user_id']
    
    doctor=tblDoctor.objects.filter(doctorID=doctor_id).first()
    user=tblUser.objects.filter(userID=user_id).first()
    if request.POST.get('btnUpdate'):
        doctor.displayName=request.POST.get('displayName')
        doctor.displayContact=request.POST.get('contact')
        doctor.bio=request.POST.get('bio')
        subCat_id=request.POST.get('subcategory')
        doctor.displayAddress=request.POST.get('address')
        doctor.mode=request.POST.get('mode')
        
        if subCat_id:
            subcategory = tblSubcategory.objects.filter(subcategoryID=subCat_id).first()
            if subcategory:
                doctor.subcategoryID = subcategory

        if user_id:
            user = tblUser.objects.filter(userID=user_id).first()
            if user:
                email=user.email
                profile=user.profilePic
                user.email=request.POST.get('email')
                user.profilePic=request.FILES.get('profile')
                user.save()
        doctor.save()
        
        # store new name in session 
        request.session['displayName'] = doctor.displayName
        request.session['profilePic'] = user.profilePic.url     
    
        return redirect(doctorProfile)  
    
    return render(request,'doctor_update_profile.html',data)

def doctorDashboard(request):
    if 'doctorID' not in request.session:
        return redirect('Login')
    
    doctor_id=request.session['doctorID']
    data={
        "doctor":tblDoctor.objects.filter(doctorID=doctor_id).first()
    }
    
    return render(request,'doctor_dashboard.html',data )

def doctorAppointments(request):
    if 'doctorID' not in request.session:
        return redirect('Login')
    doctor_id=request.session['doctorID']
    appointments=tblAppointment.objects.filter(doctorID=doctor_id)
    data={
        "doctor":tblDoctor.objects.filter(doctorID=doctor_id).first(),
        "Appointments":appointments
    }        
    return render(request,'doctor_myAppointments.html',data)

def acceptAppointment(request, id):
    if 'doctorID' not in request.session:
        return redirect('Login')
    
    appointment = tblAppointment.objects.filter(appointmentID=id).first()
    if appointment:
        appointment.isAccepted = True
        appointment.isRejected = False
        appointment.save()
    
    return redirect('doctorAppointments')

def rejectAppointment(request, id):
    if 'doctorID' not in request.session:
        return redirect('Login')
    
    appointment = tblAppointment.objects.filter(appointmentID=id).first()
    if appointment:
        appointment.isAccepted = False
        appointment.isRejected = True
        appointment.save()
    
    return redirect('doctorAppointments')

def patientDashboard(request):   
    return render(request,'patient_dashboard.html')

def patientDoctorsList(request):   
    search_query = request.GET.get('search_query', '').strip()
    
    doctors = tblDoctor.objects.all()
    
    # Agar search query hai to filter karo, warna sab doctors dikhao
    if search_query:
        doctors = doctors.filter(
            models.Q(displayName__icontains=search_query) |
            models.Q(subcategoryID__subcategoryName__icontains=search_query) |
            models.Q(userID__cityID__cityName__icontains=search_query) |
            models.Q(bio__icontains=search_query)
        )
    
    # Annotate average rating for each doctor
    doctors = doctors.annotate(avg_rating=Avg('tblreview__rating'))
    
    data = {
        "doctors": doctors,
        "search_query": search_query,
    }
    return render(request, 'patient_search_doctors.html', data)
    
def patientAppointments(request):
    return render(request, 'patient_book_appointment.html')


def doctorReviews(request):
    if 'doctorID' not in request.session:
        return redirect('Login')
    
    doctor_id = request.session['doctorID']
    doctor = tblDoctor.objects.filter(doctorID=doctor_id).first()
    reviews = tblReview.objects.filter(doctorID=doctor).order_by('-createdDT')
    
    avg_rating_dict = reviews.aggregate(Avg('rating'))
    avg_rating = avg_rating_dict['rating__avg'] or 0.0
    
    data = {
        "doctor": doctor,
        "reviews": reviews,
        "review_count": reviews.count(),
        "avg_rating": round(avg_rating, 1)
    }
    return render(request, 'doctor_reviews.html', data)

def doctorMessages(request):
    if 'doctorID' not in request.session:
        return redirect('Login')
    
    doctor_id=request.session['doctorID']
    data={
        "doctor":tblDoctor.objects.filter(doctorID=doctor_id).first(),
    }        
    return render(request,'doctor_messages.html',data)