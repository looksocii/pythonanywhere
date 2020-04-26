from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# ----------------------- ตั้งค่าที่ตั้งที่ใช้เก็บไฟล์รูปที่อัพโหลดลงบนหน้าเว็บ ---------------------- #
location = 'media/'
# ------------------------------------------------------------------------------------ #

"""
    ตาราง ACCOUNT ให้เป็นตาราง User จาก auth ของ django
    แบ่งกลุ่ม permission เป็น 2 กลุ่ม คือ บัญชีของพนักงานห้างและบัญชีของบริษัท
    ซึ่งบัญชีของพนักงานห้างจะถูกสร้างขึ้นโดย admin เท่านั้น, บัญชีของบริษัท user จะสมัครเข้ามาใช้งาน
"""

"""
    - พนักงานจะถูกเพิ่มด้วย Admin และเลือกประเภทเป็น Employee
    - เมื่อลูกค้าสมัครเข้ามาจะถูกตั้งค่าให้เลือกประเภทเป็น Company
"""
EMPLOYEE = 'EMP'
COMPANY = 'COM'
ACCOUNT_TYPE = [
    (EMPLOYEE, 'Employee'),
    (COMPANY, 'Company'),
]

"""
    พนักงานบัญชีและพนักงานฝ่ายขายจะถูกเลือกประเภทของพนักงานโดย Admin
"""
ACCOUMTANT = 'ACC'
SALE = 'SALE'
EMPLOYEE_TYPE = [
    (ACCOUMTANT, 'Accountant'),
    (SALE, 'Sale'),
]

class Department(models.Model): # ข้อมูลแผนกงาน
    """
        เพิ่มข้อมูลแผนกงานโดย admin
        (ไม่สร้าง form)
    """
    dep_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(10)]) #กำหนดให้ใส่ได้แค่ 10 หลัก
    dep_name = models.CharField(max_length=255)

    def __str__(self):
        return self.dep_name

class Employee(models.Model): # ข้อมูลพนักงานห้าง
    """ 
        - ข้อมูล Employee จะถูกสร้างโดย admin
        - emp_fname, emp_lname ใช้ตาราง User จาก auth
        - พนักงานแบ่งกลุ่ม permission ออกเป็นพนักงานฝ่ายบัญชีและพนักงานฝ่ายขาย
        ซึ่งจะถูกนำเข้ากลุ่มโดย admin กำหนด permission โดย admin
        (ไม่สร้าง form)
    """
    emp_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(10)]) #กำหนดให้ใส่ได้แค่ 10 หลัก และ ยังไม่ได้ใส่ key AI
    entrance_date = models.DateField()
    leave_date = models.DateField(blank=True, null=True)
    days_left = models.IntegerField(
        validators=[MaxValueValidator(10)], 
        auto_created=5
    ) #กำหนดให้ใส่ได้แค่ 10 หลัก และ เพิ่มข้อมูลเองโดยแต่ละคนมีวันที่ลาได้ 5 วัน
    salary = models.FloatField()
    bonus = models.FloatField(null=True)
    reimburse = models.FloatField(null=True)
    acc_type = models.CharField(max_length=255, choices=ACCOUNT_TYPE, default=EMPLOYEE) #ตั้งค่า default ให้เป็นพนักงาน
    # --------------------------------------- มีความสัมพันธ์กับตารางอื่น ---------------------------------------
    account_acc_id = models.OneToOneField(User, on_delete=models.CASCADE)
    department_dep_id = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.account_acc_id.first_name

class Manager(models.Model): # ข้อมูลผู้จัดการร้านค้า
    """
        ข้อมูลผู้จัดการถูกสร้างโดย user
        ซึ่งจะถูกสร้างหลังจากที่กรอก form สร้างบริษัทแล้ว (ต้องกำหนดว่าใครเป้นคนจัดการบริษัทนี้)
        (สร้าง form)
    """
    manag_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(10)]) #กำหนดให้ใส่ได้แค่ 10 หลัก
    manag_fname = models.CharField(max_length=255)
    manag_lname = models.CharField(max_length=255)
    manag_level = models.IntegerField(validators=[MaxValueValidator(10)]) #กำหนดให้ใส่ได้แค่ 10 หลัก
    manag_phone = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.manag_fname+' '+self.manag_lname

class Company(models.Model): # ข้อมูลบริษัท
    """
        เมื่อ user สมัครสมาชิกเสร็จแล้วจะยังไม่ทำการสร้างข้อมูล Company แต่จะมี Account แล้ว
        และจะมีปุ่มเพิ่มบริษัทหรือเริ่มเช่าพิ้นที่จะมี form ให้กรอกซึ่งเป้นข้อมูล Company
        (สร้าง form)
    """
    company_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(10)]) #กำหนดให้ใส่ได้แค่ 10 หลัก
    company_name = models.CharField(max_length=255)
    company_address = models.TextField()
    company_phone = models.CharField(max_length=9, unique=True)
    contract_fname = models.CharField(max_length=255)
    contract_lname = models.CharField(max_length=255)
    expires_date = models.DateTimeField(default=datetime.now()+timedelta(days=365)) #ต้องกำหนดว่า เวลาปัจจุบัน + 1 ปี
    other_notes = models.TextField()
    acc_type = models.CharField(max_length=255, choices=ACCOUNT_TYPE, default=COMPANY) #ตั้งค่า default ให้เป็นบริษัทที่จะมาเช่าพื้นที่
    # --------------------------------------- มีความสัมพันธ์กับตารางอื่น ---------------------------------------
    account_acc_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name

class Accountant(models.Model): # ข้อมูลพนักงานฝ่ายบัญชี
    """
        ข้อมูลพนักงานฝ่ายบัญชีจะถูกสร้างขึ้นโดย admin
        (ไม่สร้าง form)
    """
    position = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, unique=True)
    emp_type = models.CharField(max_length=255, choices=EMPLOYEE_TYPE, default=ACCOUMTANT) #ตั้งค่า default ให้เป็นพนักงานฝ่ายบัญชี
    # --------------------------------------- มีความสัมพันธ์กับตารางอื่น ---------------------------------------
    employee_emp_id = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.employee_emp_id.account_acc_id.first_name

class Sale(models.Model): # ข้อมูลพนักงานฝ่ายขาย
    """
        ข้อมูลพนักงานฝ่ายขายจะถูกสร้างขึ้นโดย admin
        (ไม่สร้าง form)
    """
    position = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, unique=True)
    emp_type = models.CharField(max_length=255, choices=EMPLOYEE_TYPE, default=SALE) #ตั้งค่า default ให้เป็นพนักงานฝ่ายขาย
    # --------------------------------------- มีความสัมพันธ์กับตารางอื่น ---------------------------------------
    employee_emp_id = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.employee_emp_id.account_acc_id.first_name

class Store(models.Model): # ข้อมูลร้านค้า
    """
        ข้อมูลร้านค้าถูกสร้างโดย user หลังจากที่กรอกข้อมูลบริษัทแล้ว (user กดปุ่มเพิ่มร้านค้า)
        (สร้าง form)
    """
    store_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(10)]) #กำหนดให้ใส่ได้แค่ 10 หลัก
    store_name = models.CharField(max_length=255)
    store_pic = models.ImageField(upload_to=location, default=None)
    branch = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    cost_total = models.FloatField(blank=True, null=True)
    repaired = models.CharField(max_length=255, blank=True, null=True)
    other_notes = models.TextField()
    # --------------------------------------- มีความสัมพันธ์กับตารางอื่น ---------------------------------------
    manage_manag_id = models.ForeignKey(Manager, on_delete=models.CASCADE)
    company_company_id = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.store_name

class Cost(models.Model): # ข้อมูลค่าใช้จ่าย
    """
        ข้อมูลการเงินจะถูกสร้างขึ้นโดยพนักงานฝ่ายบัญชี
        (สร้าง form)
    """
    cost_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(10)]) #กำหนดให้ใส่ได้แค่ 10 หลัก
    electric_bill = models.FloatField()
    water_bill = models.FloatField()
    rent_fee = models.FloatField()
    repair_fee = models.FloatField()
    insurance_fee = models.FloatField()
    other_fee = models.FloatField()
    date = models.DateField(auto_now=True)
    # --------------------------------------- มีความสัมพันธ์กับตารางอื่น ---------------------------------------
    accountant_employee_emp_id = models.ForeignKey(Accountant, on_delete=models.CASCADE)
    store_store_id = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.store_store_id.store_name

class Aperture(models.Model): # ข้อมูลพื้นที่ห้องว่าง
    """
        พื้นที่ว่างถูกเพิ่มโดยพนักงานฝ่ายขายซึ่งพนักงานฝ่ายขายถูกสร้างโดย admin
        (สร้าง form)
    """
    aper_id = models.AutoField(primary_key=True, validators=[MaxValueValidator(10)]) #กำหนดให้ใส่ได้แค่ 10 หลัก
    aper_area = models.FloatField()
    aper_loc = models.CharField(max_length=255)
    aper_pic = models.ImageField(upload_to=location, default=None)
    aper_price = models.FloatField()
    aper_status = models.BooleanField(null=False)
    issue_date = models.DateField(auto_now=True) #เพิ่มข้อมูลเองโดยเวลาที่สร้างเป็นเวลาปัจจุบัน
    # --------------------------------------- มีความสัมพันธ์กับตารางอื่น ---------------------------------------
    sale_employee_emp_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    store_store_id = models.ForeignKey(Store, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.aper_loc