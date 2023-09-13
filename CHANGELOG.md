## Changelog

##### [v2.0.0](https://github.com/nickythelion/manokit/releases/tag/v2.0.0) - Latest
**New features**
-   Added the ability to CC emails
-   Added the ability to BCC emails
-   Added the ability to customize the filesize limit. Also changed the default limit to 25 MB.
-   Added method chaining support

**Bugfixes and improvements**
-   Overhauled API. Removed both `SimpleEmail` and `HTMLEmail` and merged their functionality into the base class
-   Improved the handling of the filesize limit
-   Moved away from the `op.<property> = <value>` syntax. Replaced with proper setter functions
-   Reduced the amount of custom exceptions on favor of in-built ones
-   Improved code readability
-   Added tests
-   Improved code documentation
-   Abandoned explicit type-checking
-   Adjusted email validation regex to be more precise
-   Removed the ability to encode emails as `text/plain`. Now every email is encoded as `text/html`
-   Module clean up. The `_internal` module was removed and its functionality trimmed, refined and incorporated into the base class
-   Added the `logout()` function to properly close the session

##### [v1.2.1](https://github.com/nickythelion/manokit/releases/tag/v1.2.1)

**Bugfixes and improvements:**

-   SimpleEmail.body_from_file() and HTMLEmail.body_from_file() methods are now static. It removes inconsistency in assigning. Now all attributes (body, attachments, subject, recipients) are now assigned via `op.<property> = <value>` type of expression.

-   Fixed an issue with BodyError message not being formatted as expected.

-   Filepaths (attachments, etc) have been converted into POSIX-like paths (with forward slashes as separators) instead of being system-dependent. It insures greater readability and prevents some unexpected behaviours.

##### [v1.1.1](https://github.com/nickythelion/manokit/releases/tag/v1.1.1)

**Bugfixes and improvements:**

-   Minor bugfix with certain types (tuple, set, ...) generating runtime error when being used in type hints for variables in a subscriptable manner (tuple[str], set[str], ...). This has been fixed by this release.

##### [v1.1.0](https://github.com/nickythelion/manokit/releases/tag/v1.1.0)

**New features:**

-   Added filesize restrictions. Attachment files now cannot be larger than 20Mb. This limit cannot be disabled/overridden/etc

##### [v1.0.0](https://github.com/nickythelion/manokit/releases/tag/v1.0.0) - Initial release

**New features:**

-   Added ability to send plain-text emails
-   Added ability to send emails containing HTML
-   Added support for multiple attachments per one email
-   Added support for multiple recipients per one email
