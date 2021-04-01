### Table of contents

-   [Introduction](#introduction)
-   [Installation](#installation)
-   [Package overview](#package-overview)
-   [Simple Emails](#simple-emails)
    -   [SimpleEmail code examples](#simpleemail-code-examples)
-   [Emails with HTML](#emails-with-html)
    -   [HTMLEmail code examples](#htmlemail-code-examples)
-   [Similarity is key](#similarity-is-key)
-   [Changelog](https://github.com/NickolaiBeloguzov/manokit/blob/master/CHANGELOG.md)

### Introduction

**Manokit** is an easy-to-use native email sender for Python. That's right! _There is no dependencies!_

With just a few lines of code you will be able to send fancy emails with no headache in sight!

### Installation

You can install this package directly from [PyPI](https://pypi.org/project/manokit) or using pip:

```
pip install manokit
```

Also you can download installation-ready archives and project's source code from the [Releases](https://github.com/NickolaiBeloguzov/manokit/releases) page.

### Package overview

Manokit consists of **2** modules: _manokit.email_ provides all the functionality needed to send emails fast and simple and _manokit.exceptions_ contains all custom exceptions that can be raised by this package in case something goes wrong.

Here's a each module's struncture

-   **_*manokit.email*_ module**:

    -   _SimpleEmail_ class for sending plain-text emails
    -   _HTMLEmail_ class for sending emails containing HTML
    -   _BaseEmail_ class for development and expansion purposes

-   **_manokit.exceptions_ module**:
    -   _NotAValidEmailAddressError_ - sender's or recepient's email address is not valid (it may be a typo, missing domain, etc)
    -   _AttachmentError_ - there's an error with email's attachment file. It may point that file does not exist, is not a file or cannot be accessed.
    -   _BodyError_ - there's a problem with email's body. It may contain 'bad' characters, etc.
    -   _ParameterError_ - one or more of function's parameters are invalid. They can be of wrong type, have 'bad' values, etc
    -   _AuthError_ - there's a problem during authentication. It may indicate bad credentials or that mail server is restricting connections from an unverified source (like GMail does)
    -   _SMTPError_ - there sre some problems with SMTP connection. It may indicate faulty SMTP server, unsupported type of connection, etc.
    -   _EmailError_ - email cannot be sent. It is caused by missing metadata (subject, recepients, body, ...)

### Simple Emails

To send a very simple plain-text email you need to import _SimpleEmail_ class from _manokit.email_ module.

To initialize it, you need to pass 4 things: an SMTP server address, its port, your credentials and enable SSL (optional).

It looks like this (e.g. send an email via GMail):

```python
from manokit.email import SimpleEmail

op = SimpleEmail('smtp.gmail.com', 465, ('sender_email@gmail.com', 'TotallySecure1'), True)
```

It'll automatically authenticate you.

Note that this class does not support email with HTML in any way and will raise an exception if it detects it. The reason is that _HTMLEmail_ class is designed to work with HTML and therefore is more optimized. Simply put, _SimpleEmail_ is just not designed for HTML.

A bit of clarification. Near class' properties you can see two different specifiers: '(property)' means that you cannot change this property after instance creation; '(property + setter)' means that you can change this property's value by this expression:

```python
op.property_name = <your_value>
```

Here's a complete list of class' methods and properties:

-   **SimpleEmail**

    -   **_subject (property + setter)_**
        Email's subject line. By default it is None.
    -   **_timestamp (property)_**
        Email's time of birth, basically. It indicates exact time when class' instance was created and is used as email's time metadata
    -   **_filesize_limit (property)_**
        Maximum attachment's filesize. It is equal to 20 Mb because this is the most common limit. If file is larger, an _AttachmentError_ exception is raised. This limit cannot be disabled.
    -   **_body (property + setter)_**
        Email's body. By default it is None.
        _Note: if there are any HTML tags, a BodyError exception will be raised_
    -   **_recepients (property + setter)_**
        Addressed who will receive this email. This can take form of a single string or a list of strings. All emails are checked for validity and a _NotAValidEmailAddressError_ exception is raised if one of emails is not valid.
    -   **_attachments (property + setter)_**
        Email's attachments. You can specify an unlimited number of files to attach in form of a list of their path. They can be relative because manokit automatically converts them to absolute.
    -   **_sender_email (property)_**
        Sender's Email address.
    -   **_send() -> None (method)_**
        Sends an email. Simple as that. It takes all the parameters from properties specified above and does all the dirty work, like setting headers, behind the scenes.
    -   **_body_from_file(file: str) -> None (static method)_**
        Reads file's contents and uses it as email's body.
        File: str - path to file
        If HTML tags are detected in file's contents, an exception will be raised.

#### SimpleEmail code examples

Sendind a very basic email:

```python
from manokit.email import SimpleEmail

# Initializing
op = SimpleEmail('smtp.gmail.com', 465, ('my_email@gmail.com', 'MyPasswd1'), True)

# Setting all the important parts
# By the way, you can change any of these parameters at any time
op.subject = 'A very basic email with Manokit'
op.body = "This is a very basic letter sent to you via Manokit"
op.recepients = ['your_coworker@gmail.com', 'your_pm@hotmail.com']

# Sending email
op.send()
```

Sending a basic email with attachments:

```python
from manokit.email import SimpleEmail

# Initializing
op = SimpleEmail('smtp.gmail.com', 465, ('my_email@gmail.com', 'MyPasswd1'), True)

# Setting all the necessary parameters
op.subject = 'Quaterly Report'
op.body = "Here's the quaterly report for Q1 2021. Sending in PDF and DOCX formats"
op.recepients = 'cfo@bigcorp.com'

# Adding attachments
op.attachments = ['./report.pdf', './report.docx']

# Sending email
op.send()
```

Reading email's body from file

```python
from manokit.email import SimpleEmail

# Initializing
op = SimpleEmail('smtp.gmail.com', 465, ('my_email@gmail.com', 'MyPasswd1'), True)

# Setting all the necessary parameters
op.subject = 'A Screenplay Draft'
op.body = SimpleEmail.body_from_file('./screenplay/draft.txt')
op.recepients = 'publisher@publish.org'

# Sending email
op.send()
```

### Emails with HTML

To send fancy emails you'll need to use _HTMLEmail_ class from _manokit.email_ module.

This class lets you use HTML and inline styling to make boring text very engaging.

To initialize it, you need to pass 4 things: an SMTP server address, its port, your credentials and enable SSL (optional).

It is very similar to _SimpleEmail_.

```
from manokit.email import HTMLEmail

op = HTMLEmail('smtp.gmail.com', 465, ('sender_email@gmail.com', 'TotallySecure1'), True)
```

Here's a complete list of class' methods and properties:

-   **HTMLEmail**

    -   **_subject (property + setter)_**
        Email's subject line. By default it is None.
    -   **_timestamp (property)_**
        Email's time of birth, basically. It indicates exact time when class' instance was created and is used as email's time metadata
    -   **_filesize_limit (property)_**
        Maximum attachment's filesize. It is equal to 20 Mb because this is the most common limit. If file is larger, an _AttachmentError_ exception is raised. This limit cannot be disabled.
    -   **_body (property + setter)_**
        Email's body. By default it is None.
        _Note: if there are no HTML tags present in the body, default styling is applied. It changes font family to Verdana and text color to #262626_
    -   **_recepients (property + setter)_**
        Addressed who will receive this email. This can take form of a single string or a list of strings. All emails are checked for validity and a _NotAValidEmailAddressError_ exception is raised if one of emails is not valid.
    -   **_attachments (property + setter)_**
        Email's attachments. You can specify an unlimited number of files to attach in form of a list of their path. They can be relative because manokit automatically converts them to absolute.
    -   **_sender_email (property)_**
        Sender's Email address.
    -   **_send() -> None (method)_**
        Sends an email. Simple as that. It takes all the parameters from properties specified above and does all the dirty work, like setting headers, behind the scenes.
    -   **_body_from_file(file: str) -> None (static method)_**
        Reads file's contents and uses it as email's body.
        File: str - path to file
        If no HTML tags are found, default styling is applied.

#### HTMLEmail code examples

Sendind a simple HTML email:

```python
from manokit.email import HTMLEmail

# Initializing
op = HTMLEmail('smtp.gmail.com', 465, ('my_email@gmail.com', 'MyPasswd1'), True)

# Setting all the important parts
op.subject = 'A HTML Email with Manokit'
# HTML can be partial (without <html> and <body> tags)
op.body = """\
    <div>
        <span style="color: pink;">Here you can put basically anything</span>
    </div>
    <a href='https://github.com/NickolaiBeloguzov/manokit'>Manokit is awesome</a>
"""
op.recepients = ['mom@gmail.com', 'dad@hotmail.com']

# Sending email
op.send()
```

Sending a HTML email with attachments:

```python
from manokit.email import HTMLEmail

# Initializing
op = HTMLEmail('smtp.gmail.com', 465, ('my_email@gmail.com', 'MyPasswd1'), True)

# Setting all the necessary parameters
op.subject = 'Website patch (final)'
op.body = """\
    <div id="files">
        Here are all my files I'm sending you:
        <ul>
            <li>template.html - A site template</li>
            <li>template.css - Styles for the template</li>
            <li>main.js - Main template script</li>
        </ul>

        <span style="color: red; font-weight: bold;">
            These files must be in the same folder
        </span>
    </div>
    """
op.recepients = 'cfo@bigcorp.com'

# Adding attachments
op.attachments = ['./site/template.html', './site/template.css', './site/main.js']

# Sending email
op.send()
```

Reading email's body from file

```python
from manokit.email import HTMLEmail

# Initializing
op = HTMLEmail('smtp.gmail.com', 465, ('my_email@gmail.com', 'MyPasswd1'), True)

# Setting all the necessary parameters
op.subject = 'Your subscription has ended!'
op.body = HTMLEmail.body_from_file('./email-templates/sub-end.html')
op.recepients = 'user184720@musicforlife.com'

# Sending email
op.send()
```

### Similarity is key

You might've noticed that _SimpleEmail_ and _HTMLEmail_ are very similar in terms of used methods and their general implication. This similarity exists because all these classes are based on top of one main _BaseEmail_ class that actually contains all the functionality.

That opens up new doors for **YOU!** Yes! With Manokit you can build your own better email sending libraries. Simply inherit the _BaseEmail_ class and go beyond anyone's expectations

Here's how it works:

```python
from manokit.email import BaseEmail

class BetterEmail(BaseEmail):
    def __init__(self, host, port, creds, ssl, **kwargs) -> None:
        # do your own super cool stuff
        super().__init__(host, port, creds, ssl)

    # Override superclass methods to be better
    def send() -> None:
        print('Sending emails to {recs}..'.format(recs=', '.join(self._recepients))

        # Even more super cool stuff

        super().send()
```

### Got questions or ideas?

That's great. This means that this project is alive.

You can start by opening a [Pull Request](https://github.com/NickolaiBeloguzov/manokit/pulls) and describe your problem/suggestion/idea there.

For now that's all! But not for long...

### Changelog

To see our changelog [click here](https://github.com/NickolaiBeloguzov/manokit/blob/master/CHANGELOG.md)
