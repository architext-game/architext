# Localization
Localization is made using the [babel command line interface](http://babel.pocoo.org/en/latest/cmdline.html) and the [gettext module](https://docs.python.org/3/library/gettext.html#module-gettext).

## Writing localizable strings
When writing code, just wrap strings that should be localized with the `_()` function. This function is "installed" in the architext module `__init__.py`. Because of this it is the globally available within that module. No imports are required to use it.

You can wrap:
* Simple `""` or `''` strings.
* `"""` or `'''` multiline strings.
* `f strings` with simple expresions embedded. The expressions can't contain names from the local scope. Most global names won't be available either.

Basically you can't wrap anything else, even `textwrap.dedent()` calls. So if you need to dedent a localized string, use `textwrap.dedent(_("string"))` instead of `_(textwrap.dedent("string"))` 

## Creating the Portable Object Template file (POT) 
When you have your localizable strings, run from the root of the project
```
pybabel extract . \
    -o ./server/architext/locale/architext.pot \
    --no-wrap
```
This will create a template file for the translations, containing all strings wrapped with the `_()` function. Whenever you add new strings or modify the existing ones, you should re-create the POT file running the same command again.

## Updating the Portable Object files (PO)
PO files contain the translations for a given language. To merge the POT changes into a existing PO file use this command from the root of the project:
```
pybabel update \
    --domain=architext \
    --input-file ./server/architext/locale/architext.pot \
    --output-dir ./server/architext/locale/ \
    --no-wrap
```
This will merge the changes with all the existing PO files. Then you'll have to modify each PO file individually to add the new translations.

## Compiling the PO files into Machine Object (MO) files
Each PO file has to be compiled into its corresponding MO file. MO files are the final binaries that gettext uses to localize messages. To compile the PO files use this command from the root of the project:
```
pybabel compile \
    --domain=architext \
    --directory=./server/architext/locale \
    --use-fuzzy
```
Then you can run the server to see your new localized messages.

## Adding new languages
To add a new language you need to follow these steps:
1. Init a new PO file, using this command:
```
pybabel init \
    -D architext \
    -i ./server/architext/locale/architext.pot \
    -d ./server/architext/locale/ \
    -l es_ES \
    --no-wrap
```
Replace es_ES with whichever name you want to give to the locale. We prefer names like \<lowercase language code>_\<UPPERCASE COUNTRY CODE>.

2. Write the translations for the messages in the new PO file.
3. Compile the PO files as explained above.
4. To change the locale to your new language set the `locale` value in config.yml to the name you gave to the locale in step 1.

