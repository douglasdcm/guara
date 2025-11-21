Dry run configuration
=====================
Using dry run the execution does not runs the `do` method and the assertions, hence it does not hit the real drivers. 
If you don't need to hit the real drivers, for example, Selenium Web Driver, set the environment variable `DRY_RUN` to `true`

When using dry run the results from `Application.result` method are all `None`.
