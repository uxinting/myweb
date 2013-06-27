#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone

class MyUserManager(BaseUserManager):
    def create_user(self, email, password, nickname):
        """
        Creates and saves a User with the given email, password and nickname.
        """
        if not email:
            raise ValueError('User must have an email address')
        
        user = self.model(
                          email = MyUserManager.normalize_email(email),
                          nickname = nickname,
                          )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, nickname='admin'):
        """
        Creates and saves a superuser with the given email, password and nickname.
        """
        user = self.create_user(email, password, nickname)
        
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
                              verbose_name = 'email',
                              max_length = 255,
                              unique = True,
                              db_index = True,
                              )
    nickname = models.CharField(verbose_name='nick name', max_length=128)
    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['nickname']
    
    class Meta:
        db_table = 'user'
    
    def get_full_name(self):
        return self.nickname
    
    def get_short_name(self):
        return self.nickname
    
    def __unicode__(self):
        return self.nickname
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        if not self.is_active:
            return False
        return True
        
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app app_label?"
        if not self.is_active:
            return False
        return True
    
    @property
    def is_staff(self):
        return self.is_admin