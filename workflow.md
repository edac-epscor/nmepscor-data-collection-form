nmepscor-data-collection-form
=============================

# Anticipated Developer Workflow Document

1. Get working node/bower
2. Build virtualenv
3. Checkout application
4. Test
5. Setup database
6. Edit/Make Changes/Test
7. If you changed JS, save vendor_packages
8. Commit

## Getting a new copy

`git clone git@github.com:edac-epscor/nmepscor-data-collection-form.git`

## Building your development environment


Now, your development environment will probably have dependencies beyond what's
here (installing django-bower for example), will require bower.  Bower will
require node and npm.  The easiest way to actually have this work on Ubuntu is
*NEVER* to use the ubuntu node package, but instead to use the creepy way...

(If you use the ubuntu package, node will be called nodejs

```bash
curl -L https://npmjs.org/install.sh | sh
sudo npm cache clean -f
sudo npm install -g n # get latest stable node
sudo n stable  # use latest stable node
sudo npm install -g bower  # get bower
```

```bash
cd /workspace
virtualenv --no-site-packages projectname
source bin/activate
git clone git@github.com:edac-epscor/nmepscor-data-collection-form.git
cd nmepscor-data-collection-form
pip install -r requirements/local.list
cd application
```

Now you will have to get the database setup according to your needs.

```bash
vim base/settings/local.py
python manage.py test
python manage.py syncdb
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

* If you made database changes, remember to run migrations.
* If you changed javascript, make sure you ran bower_install
* Save all of the above to the subversion repo.  At some point, this should be a /prod/ branch

## Deploy to staging

Use our svn://ansible/epscorform.yml against test-server
`ansible-playbook -i single-server epscorform.yml`

## Deploy to prod

Not yet written as it's not decided what host this is on.  Probably a one time
occurrence as we won't be deploying that server with a new MySQL or Drupal
installation any time in the anticipated future.

## Update prod

1. Backups backups backups
2. Stop Apache
3. Checkout new copy of source tree
4. `python manage.py syncdb` Run syncdb if appropriate
5. `python manage.py migrate` Run migrations if appropriate
6. `python manage.py collectstatic`  (you did check updated vendorJS in right?)
7. Start Apache

