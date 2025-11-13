# needle_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist

from .models import Configuration

def home(request):
    """Landing page with two card buttons (you already had this)."""
    return render(request, 'needle_app/home.html')


def _get_latest_config():
    """Return the most recently created configuration."""
    return Configuration.objects.order_by('-created_at').first()

def configuration(request):
    """Display selected configuration, or the latest one by default."""
    config_id = request.GET.get("id")

    if config_id:
        config = Configuration.objects.filter(id=config_id).first()
    else:
        config = Configuration.objects.order_by('-created_at').first()

    all_configs = Configuration.objects.all().order_by('-created_at')

    return render(request, 'needle_app/configuration.html', {
        'config': config,
        'all_configs': all_configs
    })

    

@login_required
def add_master_configuration(request):
    """Create a new configuration entry and redirect to its edit page."""
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to add configurations.")

    new_config = Configuration.objects.create(
        log_folder="logs",
        log_file="main.log",
        debug_mode=False,
        logo_name="",
        save_folder_name="savedImages",
        save_mode=True,
        number_of_camera=1,
        camera_ids="40649607",
        exposure=10000,
        classification_model="",
        resize_width=960,
        resize_height=600,
        bounding_box_thickness=10,
        header_height=50,
        plc_ip="192.168.0.1",
        rack=0,
        slot=1,
        db_number=1,
        byte_index=0,
        bitindex_dict={"stn1Read": 0, "stn1WriteOK": 1, "stn1WriteNOK": 2}
    )

    # ✅ Redirect to configuration page for this specific ID
    return redirect(f"/configuration/?id={new_config.id}")



    
    """
    Accept POST from the front-end form and update the Configuration model.
    Returns JSON so the front-end JS can show a message and reload/update UI.
    """
    config = _get_or_create_config()

    # Save fields from POST — validate minimal where needed
    # Strings
    config.log_folder = request.POST.get('log_folder', config.log_folder)
    config.log_file = request.POST.get('log_file', config.log_file)
    config.logo_name = request.POST.get('logo_name', config.logo_name)
    config.save_folder_name = request.POST.get('save_folder_name', config.save_folder_name)
    config.classification_model = request.POST.get('classification_model', config.classification_model)
    config.camera_ids = request.POST.get('camera_ids', config.camera_ids)
    config.plc_ip = request.POST.get('plc_ip', config.plc_ip)

    # Integers (safe convert)
    try:
        config.number_of_camera = int(request.POST.get('number_of_camera', config.number_of_camera))
    except (ValueError, TypeError):
        pass

    try:
        config.exposure = int(request.POST.get('exposure', config.exposure))
    except (ValueError, TypeError):
        pass

    try:
        config.resize_width = int(request.POST.get('resize_width', config.resize_width))
        config.resize_height = int(request.POST.get('resize_height', config.resize_height))
        config.bounding_box_thickness = int(request.POST.get('bounding_box_thickness', config.bounding_box_thickness))
        config.header_height = int(request.POST.get('header_height', config.header_height))
    except (ValueError, TypeError):
        pass

    # Boolean fields (checkboxes send 'on' when checked)
    config.debug_mode = True if request.POST.get('debug_mode') in ['on', 'true', '1'] else False
    config.save_mode = True if request.POST.get('save_mode') in ['on', 'true', '1'] else False

    # # PLC numeric fields
    # try:
    #    config.plc_ip = request.POST.get('plc_ip', config.plc_ip)
    # config.classification_model = request.POST.get('classification_model', config.classification_model)
    # config.number_of_camera = int(request.POST.get('number_of_camera', config.number_of_camera) or config.number_of_camera)
    # config.exposure = int(request.POST.get('exposure', config.exposure) or config.exposure)
    # config.resize_width = int(request.POST.get('resize_width', config.resize_width) or config.resize_width)
    # config.resize_height = int(request.POST.get('resize_height', config.resize_height) or config.resize_height)
    # config.bounding_box_thickness = int(request.POST.get('bounding_box_thickness', config.bounding_box_thickness) or config.bounding_box_thickness)
    # config.header_height = int(request.POST.get('header_height', config.header_height) or config.header_height)
    # config.rack = int(request.POST.get('rack', config.rack) or config.rack)
    # config.slot = int(request.POST.get('slot', config.slot) or config.slot)
    # config.db_number = int(request.POST.get('db_number', config.db_number) or config.db_number)
    # config.byte_index = int(request.POST.get('byte_index', config.byte_index) or config.byte_index)

    # except (ValueError, TypeError):
    #     pass

    # ✅ JSON field
    bitindex_json = request.POST.get('bitindex_dict')
    if bitindex_json:
        try:
            config.bitindex_dict = json.loads(bitindex_json)
        except Exception:
            pass

    config.save()

    return JsonResponse({'status': 'success', 'message': 'Configuration updated successfully!'})


def initialization(request):
    """Initialization checks page with PLC connections"""
    # Replace with actual PLC status checks
    plc_connections = [
        {'name': 'PLC Main Controller', 'status': 'connected', 'ip': '192.168.1.100'},
        {'name': 'Camera Controller 1', 'status': 'connected', 'ip': '192.168.1.101'},
    ]
    return render(request, 'needle_app/initialization.html', {'plc_connections': plc_connections})


@csrf_exempt
def run_inspection(request):
    """Start the backend inspection program"""
    if request.method == 'POST':
        # Call your backend inspection code here
        return JsonResponse({'status': 'success', 'message': 'Inspection started'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def inspection_status(request):
    """Live inspection status with needle images"""
    return render(request, 'needle_app/inspection_status.html')


@csrf_exempt
def end_inspection(request):
    """End the inspection task"""
    if request.method == 'POST':
        # Stop your backend process
        return JsonResponse({'status': 'success', 'message': 'Inspection stopped'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def get_needle_images(request):
    """Return current needle images - replace with your actual backend data"""
    data = {
        'needle1': {
            'image_url': '/media/needle1_current.jpg',
            'status': 'OK',
            'defects': []
        },
     
    }
    return JsonResponse(data)


def custom_login(request):
    # If already logged in, send to configuration
    if request.user.is_authenticated:
        return redirect('configuration')   

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('configuration')   # or 'home' per your preference
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'needle_app/custom_login.html') @require_http_methods(["POST"])
 
@login_required
@require_http_methods(["POST"])
def edit_configuration(request):
    """Create a new configuration record each time user saves."""
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to edit configuration.")

    # ✅ Always create new config instead of updating old one
    config = Configuration.objects.create(
        log_folder=request.POST.get('log_folder', 'logs'),
        log_file=request.POST.get('log_file', 'main.log'),
        debug_mode=True if request.POST.get('debug_mode') == 'on' else False,
        logo_name="",
        save_folder_name=request.POST.get('save_folder_name', 'savedImages'),
        save_mode=True if request.POST.get('save_mode') == 'on' else False,
        number_of_camera=request.POST.get('number_of_camera', 1),
        camera_ids=request.POST.get('camera_ids', '40649607'),
        exposure=request.POST.get('exposure', 10000),
        classification_model=request.POST.get('classification_model', ''),
        resize_width=request.POST.get('resize_width', 960),
        resize_height=request.POST.get('resize_height', 600),
        bounding_box_thickness=request.POST.get('bounding_box_thickness', 10),
        header_height=request.POST.get('header_height', 50),
        plc_ip=request.POST.get('plc_ip', '192.168.0.1'),
        rack=request.POST.get('rack', 0),
        slot=request.POST.get('slot', 1),
        db_number=request.POST.get('db_number', 1),
        byte_index=request.POST.get('byte_index', 0),
        bitindex_dict={"stn1Read": 0, "stn1WriteOK": 1, "stn1WriteNOK": 2}
    )

    return JsonResponse({'status': 'success', 'message': 'New configuration saved successfully!'})
    

def configuration_view(request):
     return render(request, 'configuration.html')

    
