from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import pytz


# Create your models here.


class Product(models.Model):

    codes = (
        ('hood-001', 'hood-001'),
        ('hood-002', 'hood-002'),
        ('hood-003', 'hood-003'),
        ('jean-001', 'jean-001'),
        ('sock-001', 'sock-001'),
        ('head-001', 'head-001'),
    )
    code = models.CharField(choices=codes, max_length=8)
    name = models.CharField(max_length=50)
    description = description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=0, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=0)
    sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('F', 'Free'),
    )
    size = models.CharField(choices=sizes, max_length=1)

    def __str__(self):
        return f"{self.get_code_display()} / {self.name}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.stock_quantity = 0
        super(Product, self).save(*args, **kwargs)
        # 생성될 때 stock quantity를 0으로 초기화 로직


class Inbound(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)])
    received_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.received_at:
            self.received_at = timezone.now().astimezone(pytz.timezone('Asia/Seoul'))
        if not self.pk:
            self.product.quantity += self.quantity
            self.product.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} / 입고량 : {self.quantity} / 입고시간 : {self.received_at.astimezone(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M')}"


class Outbound(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)])
    shipped_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.shipped_at:
            self.shipped_at = timezone.now().astimezone(pytz.timezone('Asia/Seoul'))
        if not self.pk:
            if self.product.quantity >= self.quantity:  # 현재 재고 수량 체크
                self.product.quantity -= self.quantity
                self.product.save()
            else:
                raise ValueError("재고가 부족합니다.")
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} / 출고량 : {self.quantity} / 출고시간 : {self.shipped_at.astimezone(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M')}"
