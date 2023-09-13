# Manokit

## Table of contents
- [General Information](#general-information)
- [Installation](#installation)
- [v1 vs. v2](#v1-vs-v2)
- [Structure](#structure)
    - [Email class](#email-class)
        - [Initialization](#initialization)
        - [Authentication](#authentication)
        - [Adding recipients](#adding-recipients)
        - [Composing an email](#composing-an-email)
        - [Adding attachments](#adding-attachments)
        - [Attachment size limit](#attachment-size-limit)
        - [Sending an email](#sending-an-email)
        - [Method chaining](#method-chaining)
    - [Exceptions](#exceptions)
        - [NotAValidEmailAddressError](#notavalidemailaddresserror)
        - [EmailError](#emailerror)
        - [AttachmentError](#attachmenterror)
- [Changelog](#changelog)

## General information
Manokit is a simple, fully native library for sending emails. It provides an easy-to-use API for creating and sending emails, as well as offers a very customizable structure.

Manokit provides 2 modules: the base module name `manokit`, where the `Email` base class is defined, and a module called `manokit.exceptions` where custom exceptions, used by manokit, are defined.

## Installation
Manokit can be installed from the [PyPI](https://pypi.org/project/manokit) using the following command:
```
pip install manokit
```
You can also download the package from the [releases](https://github.com/nickythelion/manokit/releases) section, or assemble it from source.

## V1 vs. V2
Manokit has reached a point of version separation. Manokit v2's API has been overhauled to provide a more consistent and predictable experience.

These changes include:
- All functionality has been moved to a single class, instead of being scattered across 3 classes.
- Explicit type checking was removed
- Complete overhaul of properties and their behaviours

See additional info in our [Changelog](https://github.com/nickythelion/manokit/blob/master/CHANGELOG.md).

All these changes and updates are aimed at bringing a more pleasant experience to the end user, but they break compatibility. If you are currently using manokit and want to upgrade, make sure to update your codebase accordingly.

## Structure

This section describes the parts of Manokit, and how to use them.

### Email class
The `Email` class is where all the functionality resides.

#### Initialization
To begin working with Manokit, simply import the `Email` class and create an instance.
```python
from manokit import Email

email = Email(smtp_host="smtp.gmail.com", smtp_port=587)
```
During initialization you can also adjust the attachment size limit (see [attachment size limit](#attachment-size-limit) for details), by specifying the new limit in bytes, like this:
```python
from manokit import Email

small_email = Email("smtp.gmail.com", 587, filesize_limit=100)
```
In the example above we have reduced the attachment size limit from 25 MB to 100 bytes. 

#### Authentication
In order to send an email, the client must first authenticate themselves with their SMTP server. Using Manokit, the authentication process looks like this:
```python
from manokit import Email

email = Email("smtp.gmail.com", 587)
email.login(username="manokit@gmail.com", password="manokit_is_cool")
```
> This example passes the credentials as plain text for the sake of illustration.
> **Please use environment variables/other secure ways of storing credentials when logging in!**

As of May 30, 2022, Google introduced [some changes to their API](https://support.google.com/accounts/answer/6010255) that now require users to have an App Password. Manokit supports logging in with your App Password. Just pass your App Password instead of your regular password, like this:
```python
from manokit import Email

email = Email("smtp.gmail.com", 587)
email.login(username="manokit@gmail.com", password="ccfv jels tttm hshe")
```
By default, Manokit uses STARTTLS to encrypt the communication and make it more secure. If you would like to use SSL instead, simply disable STARTTLS during authentication and updating the port.
```python
from manokit import Email

email = Email("smtp.gmail.com", 465)
email.login(
    username="manokit@gmail.com", 
    password="manokit_is_cool", 
    use_starttls=False,
)
```
Manokit does not support unencrypted communication over SMTP port 25.

After you have finished with Manokit, you need to call `logout()` function to close the SMTP session.
```python
from manokit import Email

email = Email("smtp.gmail.com", 465)
email.login(
    username="manokit@gmail.com", 
    password="manokit_is_cool", 
    use_starttls=False,
)

# Your email stuff

email.logout()
```

#### Adding recipients
To add an email address to the list of recipients, simply call the appropriate function:
```python
from manokit import Email

email = Email("smtp.gmail.com", 587)
email.login(username="manokit@gmail.com", password="manokit_is_cool")
email.add_recipient("buddy@examplecorp.com")

email.logout()
```
For now, you can add recipients one at a time, so for each one you need to call the `add_recipient` function separately.

If you want to CC a person instead, replace the `add_recipient` function with `add_cc`:
```python
from manokit import Email

email = Email("smtp.gmail.com", 587)
email.login(username="manokit@gmail.com", password="manokit_is_cool")
email.add_recipient("boss@examplecorp.com") # This is important
email.add_cc("buddy@examplecorp.com")

email.logout()
```
However, make sure to add at least one recipient, or else the email will not be sent.

Same thing for BCC:
```python
from manokit import Email

email = Email("smtp.gmail.com", 587)
email.login(username="manokit@gmail.com", password="manokit_is_cool")
email.add_recipient("boss@examplecorp.com")
email.add_bcc("spy@rivalcorp.com")

email.logout()
```
It is important to know that if you try to add an email address to either recipients, CC, or BCC when it already is added to one of them, **these function will have no effect**.
```python
from manokit import Email

email = Email("smtp.gmail.com", 587)
email.login(username="manokit@gmail.com", password="manokit_is_cool")
email.add_recipient("buddy@examplecorp.com")
email.add_cc("buddy@examplecorp.com")

print(len(email.rec)) # Output: 1
print(len(email.cc)) # Output: 0

email.logout()
```
#### Composing an email
A simple email consists of a subject and a body. Both of these things are set by Manokit's `set_subject` and `set_body` functions, respectively.
```python
from manokit import Email

email = Email("smtp.gmail.com", 587)
email.login(username="manokit@gmail.com", password="manokit_is_cool")
email.add_recipient("buddy@examplecorp.com")

email.set_subject("Manokit is kinda cool!")
email.set_body("Hey, you heard about that library called Manokit? I tried it and it is nice ngl. Give it a try!")

email.logout()

```
The use of these functions is not compulsory, however. Manokit defaults the subject and the body to `<no subject>` and `<no body>`, respectively.

Manokit encodes the body of an email as `text/html`, rather than `text/plain`. This allows you to use HTML markup for styling and emphasis.

#### Adding attachments
Sometimes we need to send an email with a file attached to it. To attach the file to your email, simply call the `add_attachment` function and provide a path to the file.
```python
from manokit import Email

email = Email("smtp.gmail.com", 587)
email.login(username="manokit@gmail.com", password="manokit_is_cool")
email.add_recipient("boss@examplecorp.com")
email.add_attachment("./reports/quarterly_q3_q4.pdf")

email.logout()
```
Just as with `add_recipient`, `add_bcc` and `add_cc`, the `add_attachment` function adds one file at a time.

If an attachment has already been added, or if the size of the file being attach is 0, the function will have no effect.
```python
from manokit import Email

email = Email("smtp.gmail.com", 587)
email.login(username="manokit@gmail.com", password="manokit_is_cool")
email.add_recipient("boss@examplecorp.com")
email.add_attachment("./reports/empty_report.pdf")

print(len(email.attachments)) # Output: 0

email.logout()
```
#### Attachment size limit
By default, Manokit limits the combined size of the attachments to 25 MB (can be adjusted during the [Initialization](#initialization)).

Manokit also maintains an internal counter of how much space is available for future attachments.
```python
from manokit import Email

email = Email("smtp.gmail.com", 587, filesize_limit=100)
email.login(username="manokit@gmail.com", password="manokit_is_cool")
email.add_recipient("boss@examplecorp.com")
email.add_attachment("./reports/40kb_report.txt")

print(email.available_filesize) # Output: 60

email.logout()
```
If the attachment's size exceeds the limit, an [`AttachmentError`](#attachmenterror) will be raised.

#### Sending an email
To send an email, just call `send()`
```python
from manokit import Email

email = Email("smtp.gmail.com", 587)
email.login(username="manokit@gmail.com", password="manokit_is_cool")
email.add_recipient("buddy@examplecorp.com")
email.add_cc("buddy@examplecorp.com")

email.send()

email.logout()
```
This function can raise an [`EmailError`](#emailerror) if no recipients are defined or there was a problem while sending an email.

#### Method chaining
Manokit's functions support method chaining
```python
from manokit import Email

email = Email("smtp.gmail.com", 587)
email.login(
    username="manokit@gmail.com", 
    password="manokit_is_cool",
    ).add_recipient("buddy@examplecorp.com")
    .add_cc("buddy@examplecorp.com")
    .send()
    .logout()
```
The `logout()` function, however, is considered a logical endpoint, and thus does not support method chaining. In other words, the `logout()` function must be the last to be called.

### Exceptions

#### NotAValidEmailAddressError
This exception is raised when the email address fails validation.

Functions that can raise it:
- `login()`
- `add_recipient()`
- `add_cc()`
- `add_bcc()`

#### EmailError
This exception is raised when there is a problem with the email itself. For now this exception is only raised by the `send()` function if there is no recipients or if there was a problem with sending an email

#### AttachmentError
This exception is raised when there is a problem with email's attachments. for now this exception is only raised by the `add_attachment()` function if the path provided does not point to a file or the attachment's size is larger that the available space.

## Changelog

See the full changelog [here](https://github.com/nickythelion/manokit/blob/master/CHANGELOG.md).
