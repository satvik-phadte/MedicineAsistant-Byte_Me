from django.shortcuts import render
import os
import uuid
import math
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

from .serializers import (
    UserSerializer, PharmacySerializer, MedicineSerializer,
    PrescriptionSerializer, ReminderSerializer
)

USERS = {}
PHARMACIES = {}
MEDICINES = {}
PRESCRIPTIONS = {}
REMINDERS = {}

_next_ids = {
    'user': 1,
    'pharmacy': 1,
    'medicine': 1,
    'prescription': 1,
    'reminder': 1,
}

def _next_id(kind):
    _next_ids[kind] += 1
    return _next_ids[kind] - 1

def haversine(lat1, lon1, lat2, lon2):
    # returns distance in km
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# -------------------------
# Auth endpoints (register/login)
# -------------------------
@api_view(['POST'])
def register_user(request):
    ser = UserSerializer(data=request.data)
    if not ser.is_valid():
        return Response({'error': ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    data = ser.validated_data
    # check unique email
    for u in USERS.values():
        if u['email'] == data['email']:
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    uid = _next_id('user')
    token = str(uuid.uuid4())
    user = {
        'id': uid,
        'role': data['role'],
        'name': data['name'],
        'email': data['email'],
        'password': data['password'],  # plaintext for demo only — DO NOT do this in prod
        'phone': data.get('phone',''),
        'address': data.get('address',''),
        'token': token,
    }
    USERS[uid] = user
    return Response({'message': 'User registered', 'user_id': uid, 'token': token}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    for u in USERS.values():
        if u['email'] == email and u['password'] == password:
            # refresh token
            token = str(uuid.uuid4())
            u['token'] = token
            return Response({'token': token, 'user_id': u['id'], 'role': u['role']})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# -------------------------
# Users CRUD
# -------------------------
@api_view(['GET','POST'])
def users_list_create(request):
    if request.method == 'GET':
        return Response(list(USERS.values()))
    else:
        ser = UserSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'error': ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = ser.validated_data
        uid = _next_id('user')
        token = str(uuid.uuid4())
        user = {
            'id': uid,
            'role': data['role'],
            'name': data['name'],
            'email': data['email'],
            'password': data['password'],
            'phone': data.get('phone',''),
            'address': data.get('address',''),
            'token': token,
        }
        USERS[uid] = user
        return Response(user, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def user_detail(request, user_id):
    u = USERS.get(user_id)
    if not u:
        return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return Response(u)
    if request.method == 'PUT':
        ser = UserSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'error': ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        USERS[user_id].update(ser.validated_data)
        return Response(USERS[user_id])
    if request.method == 'DELETE':
        del USERS[user_id]
        return Response({'message':'Deleted'})

# -------------------------
# Pharmacies CRUD
# -------------------------
@api_view(['GET','POST'])
def pharmacies_list_create(request):
    if request.method == 'GET':
        return Response(list(PHARMACIES.values()))
    ser = PharmacySerializer(data=request.data)
    if not ser.is_valid():
        return Response({'error': ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    data = ser.validated_data
    pid = _next_id('pharmacy')
    pharmacy = {'id': pid, **data}
    PHARMACIES[pid] = pharmacy
    return Response(pharmacy, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def pharmacy_detail(request, pharmacy_id):
    ph = PHARMACIES.get(pharmacy_id)
    if not ph:
        return Response({'error':'Pharmacy not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return Response(ph)
    if request.method == 'PUT':
        ser = PharmacySerializer(data=request.data)
        if not ser.is_valid():
            return Response({'error':ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        PHARMACIES[pharmacy_id].update(ser.validated_data)
        return Response(PHARMACIES[pharmacy_id])
    if request.method == 'DELETE':
        del PHARMACIES[pharmacy_id]
        return Response({'message':'Deleted'})

# -------------------------
# Medicines CRUD
# -------------------------
@api_view(['GET','POST'])
def medicines_list_create(request):
    if request.method == 'GET':
        return Response(list(MEDICINES.values()))
    ser = MedicineSerializer(data=request.data)
    if not ser.is_valid():
        return Response({'error':ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    data = ser.validated_data
    mid = _next_id('medicine')
    medicine = {'id': mid, **data}
    MEDICINES[mid] = medicine
    return Response(medicine, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def medicine_detail(request, medicine_id):
    m = MEDICINES.get(medicine_id)
    if not m:
        return Response({'error':'Medicine not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return Response(m)
    if request.method == 'PUT':
        ser = MedicineSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'error':ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        MEDICINES[medicine_id].update(ser.validated_data)
        return Response(MEDICINES[medicine_id])
    if request.method == 'DELETE':
        del MEDICINES[medicine_id]
        return Response({'message':'Deleted'})

# -------------------------
# Medicine search (uses pharmacy and medicine store)
# Replace this with Google Maps + Places API for production.
# -------------------------
@api_view(['GET'])
def search_medicine(request):
    name = request.query_params.get('name')
    lat = request.query_params.get('lat')
    lng = request.query_params.get('lng')
    if not name:
        return Response({'error':'Provide ?name=...'}, status=status.HTTP_400_BAD_REQUEST)

    results = []
    for med in MEDICINES.values():
        if name.lower() in med['name'].lower():
            pharm = PHARMACIES.get(med['pharmacy_id'])
            if not pharm:
                continue
            entry = {
                'pharmacy_id': pharm['id'],
                'pharmacy_name': pharm.get('name'),
                'address': pharm.get('address',''),
                'price': med.get('price',0),
                'stock': med.get('stock',0),
                'medicine_id': med['id'],
                'medicine_name': med['name']
            }
            if lat and lng and pharm.get('lat') is not None and pharm.get('lng') is not None:
                try:
                    d = haversine(float(lat), float(lng), float(pharm['lat']), float(pharm['lng']))
                    entry['distance_km'] = round(d, 2)
                except:
                    entry['distance_km'] = None
            results.append(entry)

    # If lat/lng provided, sort by distance if available
    results.sort(key=lambda r: r.get('distance_km') if r.get('distance_km') is not None else 99999)
    # NOTE: For real production, use Google Maps Places API to find pharmacies nearby by lat/lng.
    return Response(results)

# -------------------------
# Prescriptions CRUD + upload (OCR placeholder)
# -------------------------
@api_view(['GET','POST'])
def prescriptions_list_create(request):
    if request.method == 'GET':
        return Response(list(PRESCRIPTIONS.values()))
    ser = PrescriptionSerializer(data=request.data)
    if not ser.is_valid():
        return Response({'error':ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    data = ser.validated_data
    pid = _next_id('prescription')
    pres = {'id': pid, **data}
    PRESCRIPTIONS[pid] = pres
    return Response(pres, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def prescription_detail(request, presc_id):
    p = PRESCRIPTIONS.get(presc_id)
    if not p:
        return Response({'error':'Prescription not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return Response(p)
    if request.method == 'PUT':
        ser = PrescriptionSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'error': ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        PRESCRIPTIONS[presc_id].update(ser.validated_data)
        return Response(PRESCRIPTIONS[presc_id])
    if request.method == 'DELETE':
        del PRESCRIPTIONS[presc_id]
        return Response({'message':'Deleted'})

@api_view(['POST'])
def upload_prescription(request):
    # Accepts multipart/form-data: file + user_id
    f = request.FILES.get('file')
    user_id = request.POST.get('user_id')
    if f is None:
        return Response({'error':'file field required'}, status=status.HTTP_400_BAD_REQUEST)

    # Save file to MEDIA_ROOT/prescriptions/
    dest_dir = os.path.join(settings.MEDIA_ROOT, 'prescriptions')
    os.makedirs(dest_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{f.name}"
    path = os.path.join(dest_dir, filename)
    with open(path, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

    # Placeholder OCR logic:
    # TODO: Integrate real OCR (Google Cloud Vision / Tesseract). Example (pseudo):
    # from google.cloud import vision
    # client = vision.ImageAnnotatorClient()
    # with open(path, 'rb') as image_file:
    #   content = image_file.read()
    #   image = vision.Image(content=content)
    #   response = client.text_detection(image=image)
    #   ocr_text = response.text_annotations[0].description
    # For now we return a mocked OCR result:
    mocked_ocr = "Mocked OCR result: Paracetamol 500mg - 1 tab twice daily"

    # store prescription object if user provided
    pid = _next_id('prescription')
    pres = {
        'id': pid,
        'user_id': int(user_id) if user_id else None,
        'medicines': [],
        'uploaded_image_url': f"/media/prescriptions/{filename}",
        'ocr_text': mocked_ocr
    }
    PRESCRIPTIONS[pid] = pres
    return Response({'message':'Uploaded', 'ocr_text': mocked_ocr, 'prescription': pres})

# -------------------------
# Reminders CRUD
# -------------------------
@api_view(['GET','POST'])
def reminders_list_create(request):
    if request.method == 'GET':
        return Response(list(REMINDERS.values()))
    ser = ReminderSerializer(data=request.data)
    if not ser.is_valid():
        return Response({'error': ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    data = ser.validated_data
    rid = _next_id('reminder')
    rem = {'id': rid, **data}
    REMINDERS[rid] = rem
    return Response(rem, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def reminder_detail(request, reminder_id):
    r = REMINDERS.get(reminder_id)
    if not r:
        return Response({'error':'Reminder not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return Response(r)
    if request.method == 'PUT':
        ser = ReminderSerializer(data=request.data)
        if not ser.is_valid():
            return Response({'error': ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        REMINDERS[reminder_id].update(ser.validated_data)
        return Response(REMINDERS[reminder_id])
    if request.method == 'DELETE':
        del REMINDERS[reminder_id]
        return Response({'message':'Deleted'})

# -------------------------
# Doctor creates prescription
# -------------------------
@api_view(['POST'])
def doctor_create_prescription(request):
    # body must contain doctor_id, user_id, medicines list
    ser = PrescriptionSerializer(data=request.data)
    if not ser.is_valid():
        return Response({'error': ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    data = ser.validated_data
    pid = _next_id('prescription')
    data['id'] = pid
    PRESCRIPTIONS[pid] = data
    return Response({'message':'Prescription created', 'prescription': data}, status=status.HTTP_201_CREATED)

# -------------------------
# Pharmacy inventory update
# -------------------------
@api_view(['POST'])
def pharmacy_update_inventory(request):
    """
    Request body:
    {
      "pharmacy_id": 1,
      "medicines": [
         {"medicine_id": 2, "stock": 50, "price": 45},
         {"name": "NewMedicine", "brand":"BrandX", "stock": 10, "price": 120}
      ]
    }
    - Allows updating existing medicines' stock/price or creating new medicine entries tied to the pharmacy.
    """
    payload = request.data
    pid = payload.get('pharmacy_id')
    meds = payload.get('medicines', [])
    if pid not in PHARMACIES:
        return Response({'error':'Pharmacy not found'}, status=status.HTTP_404_NOT_FOUND)

    updated = []
    created = []
    for m in meds:
        if 'medicine_id' in m and m['medicine_id'] in MEDICINES:
            mid = m['medicine_id']
            MEDICINES[mid]['stock'] = m.get('stock', MEDICINES[mid].get('stock', 0))
            MEDICINES[mid]['price'] = m.get('price', MEDICINES[mid].get('price', 0))
            updated.append(MEDICINES[mid])
        else:
            # create new medicine tied to pharmacy
            mid = _next_id('medicine')
            new_med = {
                'id': mid,
                'name': m.get('name'),
                'brand': m.get('brand',''),
                'description': m.get('description',''),
                'price': m.get('price',0),
                'stock': m.get('stock',0),
                'pharmacy_id': pid
            }
            MEDICINES[mid] = new_med
            created.append(new_med)
    return Response({'updated': updated, 'created': created})