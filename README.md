# :cat: Kitty CTF - Write up
#### Author : agi-jsg 
#### Date : 05/06/2021



I realised a CTF, and I wanted to do a write up about how I finished it. :computer: 



# Pwning the website

There was a website which index.php file returned a 403 HTTP Status. Thus, the first step was to bruteforce the directories.

## Bruteforcing directories :open_file_folder:

 I decided to list every directory with the tool I developed (you can find it in the dirlisting repo). I found a directory named support which had an index.php file with a login form 

## Bruteforcing login form

After finding login form I decided to make my own program with the request library of python to post datas and I used rockyou wordlist and the output of the program was : 
```python
password admin : zxcvbnm
```

## Exploring the website :detective:

There was only a pdf viewer with archived letters :envelope:. By finding, I got a name and password in the website : 
```python
name: garizov
password: Russkaya_R0d1na
```

## Getting the first flag
```python
FL4G{k1tty-0n3-G@r1z0v}
```

# Pwning the system

I connected to the machine  :satellite: with SSH with the account  of garizov and I found an interesting file signed by someone named Richard. So I didn't waste my time with unnecessary Linux Enumeration. I just found that there were two users by digging in the ```
/home``` directory : 

 1. garizov (the pwned user)
 2. castillo (the user we want to pwn)

## Exploring the system
With the find command 
```bash
find / -name *richard* 2> /dev/null
```
I was able to discover a file :floppy_disk: : 
```bash
/media/USB-14B7/richard.img
```

## Download file to my local machine
I downloaded the file to my local machine to analyse it.
```bash
scp -P $PORT garizov@$IP:/media/USB-14B7/richard.img .
file richard.img
	#Output
	richard.img: LUKS encrypted file, ver 1 [aes, xts-plain64, sha256] UUID: 8fd504d8-5812-4e8d-886a-6c265a7ba53e
```
I had to find documentation on luks files



## Learning about luks

I decided to learn about luks on the dedicated gitlab repo which is : https://gitlab.com/cryptsetup/cryptsetup/wikis which says : 

> **LUKS** is the standard for Linux hard disk encryption. By providing a standard on-disk-format, it does not  
only facilitate compatibility among distributions, but also provides secure management of multiple user passwords.  
LUKS stores all necessary setup information in the partition header, enabling to transport or migrate data seamlessly.

## Reading the hidden data

Once I had the file how to read it ? How to decrypt it ? I didn't know any of this so I continued to search about LUKS and tried to understand how it works.

### Bruteforcing the key

https://github.com/glv2/bruteforce-luks

With the tool bruteforce-luks I found a password to decrypt the file 
```bash
bruteforce-luks -t 6 -f dictionary.txt richard.img
password : angels
```

### Decrypt file

To decrypt a luks file, we need to be sure dm-crypt kernel module was loaded with the following command then do another bunch of commands which will  create a device that we can then mount.
```bash
modprobe dm-crypt #Verification if dm-crypt kernel module was loaded
cryptsetup open --type luks richard.img random_name # "Creating" the device
mount /dev/mapper/random_name /tmp #Mounting the device
```
By executing these commands I had a id_rsa  :closed_lock_with_key:  file in my /tmp/ directory 
 then by ssh with the other account because there were only two users on the machine castillo and garizov.
 So I connected to the machine but this time into Castillo's account with the id_rsa file with the following command : 
```bash
ssh -i /tmp/id_rsa castillo@$IP -p $PORT 
cat flag.txt
	#OUTPUT
	FL4G{Kitty-two_W3_W1LL_C4TCH_TH3M_4LL}
```

