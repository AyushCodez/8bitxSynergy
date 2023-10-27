from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from django.contrib import messages
from .models import User,Code
from datetime import datetime, timedelta
d={'g_keep_thinking_guy': 100,
 'g_not_a_shaving_mirror': 100,
 'g_open_nets_are_hard': 200,
 't_three_strikes_and_out': 't10',
 't_game_of_codes': 't10',
 'g_fancy_stairs': 200,
 'g_jogging_is_hard': 200,
 'g_flagging_irl': 100,
 't_bridges_are_nice': 't10',
 'g_why_does_it_exist': 300,
 'g_christmas_cheer': 200,
 'g_pnb_is_a_bank': 300,
 'g_piped_plants': 100,
 'g_fill_the_pot': 300,
 'g_lots_of_lamps': 200,
 'g_tall_rock_no': 100,
 'g_big_brother_watching': 't10',
 'v_titanic_reference_really': 1500,
 'g_we_are_easy_to_lose': 200,
 'g_yellow_is_a_weird_colour': 300,
 'g_important_people': 100,
 'g_wish_it_was_slower': 100,
 'v_only_nerds_here': 1500,
 'g_someone_treat_me_pls': 200,
 't_liar_liar': 't10',
 'g_study_in_the_basement': 200,
 't_why_dont_the_stairs_work': 't10',
 'g_enter_at_your_own_risk': 300,
 'g_we_are_safety_hazards': 200,
 'g_good_music_taste': 400,
 'g_let_it_fall': 200,
 'g_basic_maths_passed': 100,
 'g_volleyball_be_hard': 100,
 't_crawling_time': 't10',
 'g_charlie_puth_stan': 200,
 'v_recycling_is_good': 1000,
 'g_the_tiles_are_gay': 100,
 'g_he_trying_his_best': 100,
 'v_rocks_exist': 2000,
 'g_baby_painting': 100,
 't_wish_she_noticed_me': 't10',
 'g_seven_by_two': 200,
 'g_im_thirsty': 200,
 'g_get_off_your_butt': 400,
 'g_peak_architecture': 200,
 'g_have_you_read_it': 300,
 'g_youll_be_on_this_too': 200,
 't_you_dont_know_how_i_work': 't10',
 'g_paani_paani_paani': 200,
 'g_everything_the_light_touches': 400,
 'g_glass_box': 100,
 'g_raavana_jai_jai_jai': 100,
 't_environmentalist_moment': 't10',
 'g_you_should_run_more': 200,
 'g_papaya_is_paw_paw': 400,
 'g_legal_ports_of_entry': 200,
 'g_i_belong_in_here': 100,
 'g_objects_ive_shoved_up': 200,
 'v_plants_for_camo': 1500,
 'g_wtf_is_a_kilometer': 100,
 'g_window_of_opportunity': 200,
 'g_just_spend_money': 100,
 'v_who_reads_anymore': 1500,
 'g_everyday_in_africa': 200,
 'g_go_play_in_the_field': 100,
 'g_racist_game': 100,
 't_do_you_lift': 't10',
 'g_you_think_youre_good': 100,
 'g_you_love_us_right': 100,
 'g_eating_without_youtube': 300,
 'g_i_walk_to_burger_king': 100,
 'g_the_price_is_right': 200,
 'g_i_wanted_to_be_a_doctor': 200,
 'g_hardik_pandya_op': 200,
 'g_rebel_and_speed': 100,
 'g_kitchen_nightmares': 200,
 'g_this_wash_is_on_fire': 300,
 'g_electricity_in_ecity': 100,
 't_park_here123': 't10',
 'v_pom_pom': 1500,
 'g_lilavati_softball': 100}
k_l=list(d.keys())
v_l=list(d.values())
def loginPage(request): 
    page = 'login'
    if request.user.is_authenticated:
        return redirect('participant_home') 

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('participant_home') 
        else:
            messages.error(request, 'Email OR password does not exit') 
    context = {'page': page}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if "iiitb.ac.in" in user.email: 
                user.email = user.email.lower()
                user.save()
                login(request, user)
                return redirect('participant_home')
            messages.error(request, 'Use iiitb mail id')
        else:
            messages.error(request, 'An error occurred during registration (Ensure that you are not using the same email id, this error could have been caused by that)')

    return render(request, 'login_register.html', {'form': form})

def participant_home(request):
    da=datetime.now()
    user_1= User.objects.get(email=str(request.user))
    timezone = user_1.sand.tzinfo
    da=da.replace(tzinfo=timezone)
    flag=(da<user_1.sand)
    if request.method == 'POST':
        if  not (flag):
            messages.error(request,"You can't enter code now , the contest is over")
        else:
            a=request.POST.get('text_input').strip().lower()
            passcode = list(Code.objects.filter(user=request.user).values())
            new_arr=[]
            for x in passcode:
                new_arr.append(x['data_item'])
            if a not in new_arr:
                if a in k_l:
                    Code.objects.create(
                    user=user_1,
                    data_item=a,
                    )
                    if type(d[a]) == int:
                        user_1.gold +=d[a]
                        user_1.save()
                    else:
                        return HttpResponse("Go to 8Bit checkpost and get your time increased by 10 minutes")
                else:
                    messages.error(request,'Ooops Better luck next time ')
            else:
                messages.error(request,'You have already got points for submitting the above code . This is a repeat submission') 

    users=User.objects.all().order_by('-gold').values()
    context = {
        'users': users,
        'user_1':user_1,
        'curr_date_time':str(user_1.sand.month) + " " + str(user_1.sand.day) + "," + str(user_1.sand.year) + " " + str(user_1.sand.hour) + ":" + str(user_1.sand.minute) + ":" + str(user_1.sand.second),
        'flag':flag
    }
    return render(request, 'participant_home.html', context)
