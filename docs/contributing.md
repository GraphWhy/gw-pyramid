Contributing
============

All projects under the Pylons Projects, including this one, follow the
guidelines established at [How to
Contribute](http://www.pylonsproject.org/community/how-to-contribute).

You can contribute to this project in several ways.

* [File an Issue on GitHub](https://github.com/Pylons/pyramid_blogr/issues)
* Fork this project and create a branch with your suggested change. When ready,
  submit a pull request for consideration. [GitHub
  Flow](https://guides.github.com/introduction/flow/index.html) describes the
  workflow process and why it's a good practice.
* Join the IRC channel [#pyramid on irc.freenode.net]
  (http://webchat.freenode.net/?channels=pyramid).


Prerequisites
-------------

Follow the instructions to install Pyramid and the tools needed to build its
documentation in
[HACKING.txt](https://github.com/Pylons/pyramid/blob/master/HACKING.txt). We
will leverage this virtual environment and the tools installed there to build
documentation for this project. This has several advantages:

* You don't have to install Sphinx and its dependencies another time.
* You are encouraged to contribute to the official tutorials in the Pyramid
  documentation.
    * [Quick Tutorial for Pyramid]
      (http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/index.html)
    * [Creating Your First Pyramid Application]
      (http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/firstapp.html)
    * [SQLAlchemy + URL Dispatch Wiki Tutorial]
      (http://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki2/index.html)
    * [ZODB + Traversal Wiki Tutorial]
      (http://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki/index.html)
    * [Running a Pyramid Application under mod_wsgi]
      (http://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/modwsgi/index.html)
* No increased maintenance for the Pylons Project.


Building documentation for a Pylons Project project
---------------------------------------------------

*Note:* These instructions might not work for Windows users. Suggestions to
improve the process for Windows users are welcome by submitting an issue or a
pull request. Windows users may find it helpful to follow the guide [Installing
Pyramid on a Windows System]
(http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/install.html#installing-pyramid-on-a-windows-system).

1.  Fork the repo on GitHub by clicking the [Fork] button.
2.  Clone your fork into a workspace on your local machine.

         git@github.com:<username>/pyramid_blogr.git

3.  Add a git remote "upstream" for the cloned fork.

         git remote add upstream git@github.com:Pylons/pyramid_blogr.git

4.  Set an environment variable as instructed in the
    [prerequisites](https://github.com/Pylons/pyramid/blob/master/HACKING.txt#L55-L58).

         # Mac and Linux
         $ export VENV=~/<path-to-workspace>/env

         # Windows
         set VENV=c:\<path-to-workspace>\env

5.  Try to build the docs in your workspace.

         # Mac and Linux
         $ make clean html SPHINXBUILD=$VENV/bin/sphinx-build

         # Windows
         c:\> make clean html SPHINXBUILD=%VENV%\bin\sphinx-build

    If successful, then you can make changes to the documentation. You can load
    the built documentation in the `/_build/html/` directory in a web browser.

6.  From this point forward, follow the typical git workflow.  Start by pulling
    from the upstream to get the most current changes.

         git pull upstream master

7.  Make a branch, make changes to the docs, and rebuild them as indicated in
    step 5.  To speed up the build process, you can omit `clean` from the above
    command to rebuild only those pages that depend on the files you have
    changed.

8.  Once you are satisfied with your changes and the documentation builds
    successfully without errors or warnings, then git commit and push them to
    your "origin" repository on GitHub.

         git commit -m "commit message"
         git push -u origin --all # first time only, subsequent can be just 'git push'.

9.  Create a [pull request](https://help.github.com/articles/using-pull-requests/).

10.  Repeat the process starting from Step 6.
