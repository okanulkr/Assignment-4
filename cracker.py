#!/usr/bin/env python
# coding: utf-8

# In[1]:


import hashlib # to generate md5 hash
import bcrypt # to generate random salt
import random # to generage random password_lists
import time # to get execution time
import argparse # to get arguments


# # Arguments & Setting Defaults

# In[2]:


parser = argparse.ArgumentParser()
parser.add_argument("-f")
parser.add_argument("-password", default="303030")
parser.add_argument("-dictionary_size", default=333333, type=int)
parser.add_argument("-pass_list_size", default=4000, type=int)
parser.add_argument("-i", default="moon.jpg")
args = parser.parse_args()

password_space = (0, 999999)
alices_raw_password = args.password
dictionary_size = args.dictionary_size
password_list_size = args.pass_list_size
constant_salt = bcrypt.gensalt() # randomly generated salt

print(f"Alice's raw password is:\t\t{alices_raw_password}\nSalt is:\t\t\t\t{constant_salt}")


# In[3]:


# md5 hash function that using salt above
def hash_with_constant_salt(password_string):
    password = password_string.encode('utf-8')
    return hashlib.md5(password + constant_salt).hexdigest()


# In[4]:


# hashed password of Alice
alices_hashed_password = hash_with_constant_salt(alices_raw_password)
print(f"alice's hashed password is: {alices_hashed_password}")


# # First Case

# In[5]:


def first_case(alices_hashed_password):
    for i in range(password_space[0], password_space[1]):
        padding = len(str(password_space[1]))
        candidate = str(i).zfill(padding) # zfill used for padding: 63 -> 000063
        if(alices_hashed_password == hash_with_constant_salt(candidate)):
            print(f'password cracked > {candidate}')
            return


# In[6]:


print("Case1:\n")
start_time = time.time()
first_case(alices_hashed_password)
print("--- %s seconds ---\n\n" % (time.time() - start_time))


# # Second Case

# In[7]:


def generate_dictionary():
    passwords = []
    for i in range(password_space[0], dictionary_size):
        padding = len(str(dictionary_size))
        passwords.append(str(i).zfill(padding))
    return passwords

def second_case(alices_hashed_password, dictionary):
    for i in dictionary:
        if(alices_hashed_password == hash_with_constant_salt(i)):
            print(f'password cracked > {i}')


# In[8]:


dictionary = generate_dictionary()
print("Case2:\n")
start_time = time.time()
second_case(alices_hashed_password, dictionary)
print("--- %s seconds ---\n\n" % (time.time() - start_time))


# # Third Case

# In[9]:


def generate_password_list_raw():
    password_list = []
    for i in range(0, password_list_size):
        password = random.randint(password_space[0], password_space[1])
        padding = len(str(password_space[1]))
        password_list.append(str(password).zfill(padding))
    return password_list

def third_case(password_list_with_constant_salt):
    for i in range(password_space[0], password_space[1]):
        padding = len(str(password_space[1]))
        candidate = str(i).zfill(padding)
        if(hash_with_constant_salt(candidate) in password_list_with_constant_salt):
            print(f'one password of the password list cracked > {candidate} was on password list')
            return


# In[10]:


password_list = generate_password_list_raw()
password_list_with_constant_salt = list(map(hash_with_constant_salt, password_list))
print("Case3:\n")
start_time = time.time()
third_case(password_list_with_constant_salt)
print("--- %s seconds ---\n\n" % (time.time() - start_time))


# # Fourth Case

# In[11]:


def fourth_case(password_list):
    for i in dictionary:
        if(hash_with_constant_salt(i) in password_list):
            print(f'one password of the password list cracked > {i} was on password list')
            return


# In[12]:


print("Case4:\n")
start_time = time.time()
fourth_case(password_list_with_constant_salt)
print("--- %s seconds ---\n\n" % (time.time() - start_time))

