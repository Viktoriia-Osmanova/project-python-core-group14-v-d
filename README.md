Welcome to the project 'Personal Helper'! This is console bot made by the 'Innovate Tech' team.

This bot works in three modes:

Contacts book that stores names, addresses, phones, emails and dates of birth and implements some useful search commands.
Notes. Just simple text notes with tags and search-ability.
In the CONTACTS BOOK mode, user of the 'Personal Helper' can do the following.

- Add, change and delete such contacts data as name, address, phone numbers, email and date of birth.
- Search contacts by their data.
- View contacts whose birthday is within specified period starting from today, in 2 days and in 3 days.
- View the list of all contacts in the book.

All the phones, emails and dates are being checked if they match strict rules:
- (+XXX)-XXX-XX-XX-XX for phone numbers.
- aaa@bbb.cc for emails.
- YYYY.DD.MM for dates.

In the NOTES mode, user of the 'Personal Helper' can do the following.

- Add, change and delete text notes that are being stored in the file note.txt in the same folder
  as the script file.
- Add tags to the notes.
- Search notes by keywords, tags and date ranges.

To use this bot, you need simply download setup package with all necessary files from github. Package can be installed into system with a console command "python setup.py install". After that, you can run the bot using 'personal-helper' command in any place in the command line mode.

'Personal Helper' communicates with a user through console commands. You can view them using command 'help' inside the bot.


INSTALLATION:

'Personal Helper' is being distributed in the form of Python package. You can install it using one of the following two commands in the directory with setup.py file:

pip install .
python setup.py install