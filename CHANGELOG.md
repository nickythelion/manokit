## Changelog

##### v1.2.1 - Not released yet

**New features:**

-   SimpleEmail.body_from_file() and HTMLEmail.body_from_file() methods are now static. It removes inconsistency in assigning. Now all attributes (body, attachments, subject, recepients) are now assigned via `op.<property> = <value>` type of expression.

**Bugfixes:**

-   Fixed an issue with BodyError message not being formatted as expected.

##### [v1.1.1](https://github.com/NickolaiBeloguzov/manokit/releases/tag/v1.1.1) - Latest

**Bugfixes:**

-   Minor bugfix with certain types (tuple, set, ...) generating runtime error when being used in type hints for variables in a subscriptable manner (tuple[str], set[str], ...). This has been fixed by this release.

##### [v1.1.0](https://github.com/NickolaiBeloguzov/manokit/releases/tag/v1.1.1)

**New features:**

-   Added filesize restrictions. Attachment files now cannot be larger than 20Mb. This limit cannot be disabled/overriden/etc

##### [v1.0.0](https://github.com/NickolaiBeloguzov/manokit/releases/tag/v1.0.0) - Initial release

**New features:**

-   Added ability to send plain-text emails
-   Added ability to send emails containing HTML
-   Added support for multiple attachments per one email
-   Added support for multiple recepients per one email
