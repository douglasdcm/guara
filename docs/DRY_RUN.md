# Dry run configuration
Using dry run the execution does not runs the `do` method and the assertions, hence it does not hit the real drivers. 
By default the `DRY_RUN` enviroment variable is set to `false`. If you don't need to hit the real drivers, for example, Selenium Web Driver:
1. Copy the file `.env_template` to `.env`
2. Change the value of `DRY_RUN` to `true`

When using dry run the results from `Application.result` method are all `None`.
