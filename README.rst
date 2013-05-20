VIM Setup
=========
Why not make updating VIM easier?

....

VIM Setup Documentation
=======================
I like bleeding edge software. A lot. The problem is that when it comes to my editor (VIM) I don't update it often because if my development environment breaks, then I'm hosed and have to figure out what works and what's broken. To alleviate this problem I decided to create a script that would go ahead and backup my current setup and then pull the latest plugins I use from their respective locations into a brand new .vim directory. This should make it so that if something does break I can at least use the backed up version until I have time to figure out what did break.

It grabs `pathogen`_ by default and creates a modified folder structure for use with `pathogen`_, so if you don't use `pathogen`_ (which I wouldn't understand why you wouldn't - that's why I linked to it 3 times) this probably isn't the script for you.

So how do you set it up to do what you want? There's a vim_plugins.json file in the vim_setup directory. There are two options you must specify: type and location. The type is how the plugin should be pulled it (git or curl). It only handles git and curl (though it could be re-written to support more options) because it's all I needed for the time being.

The file is self explanatory and I've populated it with the things I already use so poke around in there.

Once that's done just run the file and it'll pull down all the things you want after it backs up your current vim setup. It's fairly verbose, though at some point I'll make that an option.

=============
Code Location
=============
https://github.com/ArrantSquid/vim-setup

....

Created by `Johnny P. Neumann (ArrantSquid) <http://twitter.com/ArrantSquid>`_


.. LINKAGE

.. _`pathogen`: https://github.com/tpope/vim-pathogen

