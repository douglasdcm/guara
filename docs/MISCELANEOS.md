# Using other Web Drivers

It is possible to run Guara using other Web Drivers like [Caqui](https://github.com/douglasdcm/caqui) and [Playwright](https://playwright.dev/python/docs/intro). Check the requirements of each Web Driver before execute it. For example, Playwright requires the installation of browsers separately.

# Asynchronous execution
The core code was extended to allow asynchronous executions. Get more details [here](https://github.com/douglasdcm/guara/tree/main/docs/ASYNC.md)

# ChatGPT assistance
It is possible to use [ChatGPT](https://chatgpt.com/) to help you organize your code in `Page Transactions` pattern. Check these [simple steps](https://github.com/douglasdcm/guara/blob/main/docs/CHATGPT_ASSISTANCE.md).

# Non-Testers Usage

Page Transactions is primarily based on the Command Pattern (GoF), making it suitable for product development as well, even though that is not its primary intent. This section is dedicated to showcasing other uses of the framework that are unrelated to automation testing.

## Prototyping

Software engineers, UX designers with some knowledge of programming, and software students can leverage this project to build simple applications that are testable by default. For example, [To-Do List web application](https://github.com/douglasdcm/guara/blob/main/examples/prototyping) was built with Guara and PyScript.
