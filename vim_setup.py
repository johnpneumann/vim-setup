#!/usr/bin/env python
"""Set's up a new .vim folder structure

.. module:: vim_setup
    :platform: Unix, Linux
        :synopsis: Set's up a new .vim folder structure while backing
            up the previous version.

.. moduleauthor:: jneumann

.. note::
    None
"""
# Built In
import os
import sys
import json
import shutil
import subprocess
from datetime import datetime

# Third Party

# Custom
import generic_msg

def main():
    """Starts our vim setup.

    Args:
        None.

    Returns:
        None.

    """
    setup = VimSetup()
    setup.start_setup()

    return

class VimSetup(object):
    """Runs our setup for vim.

    Args:
        object (obj): Generic object.

    """
    def __init__(self):
        super(VimSetup, self).__init__()
        self.valid_answers = ['yes', 'no', 'y', 'n']
        self.yes_answers = ['yes', 'y']
        self.no_answers = ['no', 'n']
        self.home_dir = os.path.expanduser('~')
        self.vim_dir = os.path.join(self.home_dir, '.vim')
        self.backup_directory = None

    def start_setup(self):
        """Starts our setup.

        Args:
            None.

        Returns:
            bool. True or False on success.

        """
        backup_result = self.backup_vimdir()
        if not backup_result:
            msg = ('Could not backup vim directory. Failing.')
            generic_msg.error(msg)
            self.handle_failure()

        setup_result = self.vim_setup()
        if not setup_result:
            self.handle_failure()

        msg = ('Finished setup. Looks like it worked! Woot! '
               'Thanks for using it!')
        generic_msg.final(msg)

    def backup_vimdir(self):
        """Backs up the .vim directory

        Args:
            None.

        Returns:
            bool. True or False

        """
        self.backup_directory = os.path.join(self.home_dir, '.vim_backup')
        if os.path.exists(self.backup_directory):
            msg = ('It appears that the directory already exists. Would you '
                   'like to backup the older directory with the current '
                   'datetime appended to it? [y/n]')
            generic_msg.prompt(msg)
            input_result = raw_input().lower()
            if input_result in self.yes_answers:
                cur_date = datetime.now().strftime('%Y_%M_%d_%H_%M_%S')
                self.backup_directory = os.path.join(
                    self.home_dir, '.vim_backup_%s' % (cur_date)
                )
            else:
                msg = ('User cancelled vim setup.')
                generic_msg.info(msg)
                sys.exit(1)

        result = self.handle_moving_dirs(self.vim_dir, self.backup_directory)
        return result

    def vim_setup(self):
        """This does all of our setup to grab all the necessary data.

        Args:
            None.

        Returns:
            bool. True or False.

        """
        pathogen_dirs = ['autoload', 'bundle',
                         'colors', 'plugin']

        vimdir_result = self.handle_mkdir(self.vim_dir)
        if not vimdir_result['success']:
            generic_msg.error(vimdir_result['msg'])
            self.handle_failure()

        msg = ('Making the following '
               'directories: %s' % (', '.join(pathogen_dirs)))
        generic_msg.info(msg)
        for dirname in pathogen_dirs:
            full_dirname = os.path.join(self.vim_dir, dirname)
            dir_result = self.handle_mkdir(full_dirname)
            if not dir_result['success']:
                generic_msg.error(dir_result['msg'])
                self.handle_failure()

        plugin_result = self.get_plugins()
        if not plugin_result:
            msg = ('Something really fucked up here. We have to '
                   'kill this now.')
            generic_msg.error(msg)
            self.handle_failure()

        msg = ('We can run some cleanup and try and remove all of the '
               '.rst, .md and .markdown files now if you would like. '
               'Proceed? [y/n]')
        generic_msg.prompt(msg)
        input_result = raw_input().lower()
        if input_result in self.yes_answers:
            cleanup_result = self.handle_cleanup()
            if cleanup_result:
                msg = ('Something during the cleanup process got borked. '
                       'Not a big deal, but you should probably check '
                       'it out.')
                generic_msg.warning(msg)

        return True

    def get_plugins(self):
        """Gets the plugins we want for vim.

        Args:
            None.

        Returns:
            bool. True or False.

        """
        status_code = 0
        plugin_file = os.path.join(os.getcwd(), 'vim_plugins.json')
        with open(plugin_file, 'r') as fopen:
            try:
                vim_plugins = json.loads(fopen.read())
            except Exception as err:
                msg = ('An error occurred when attempting to parse the '
                       'json file. Error: %s' % (err))
                generic_msg.error(err)
                self.handle_failure()

        pathogen_url = ('https://raw.github.com/tpope/vim-pathogen/master'
                        '/autoload/pathogen.vim')

        result = self.handle_curl_clone(pathogen_url,
                                        os.path.join(self.vim_dir, 'autoload'))
        status_code += result

        for key, value in vim_plugins.iteritems():
            full_dirname = os.path.join(self.vim_dir, key)
            for obj in value:
                if obj['type'] == 'git':
                    result = self.handle_git_clone(
                        obj['location'], full_dirname
                    )
                    status_code += result
                elif obj['type'] == 'curl':
                    result = self.handle_curl_clone(
                        obj['location'], full_dirname
                    )
                    status_code += result
                else:
                    msg = ('No type specified. Ignoring. %s %s' % (key, obj))
                    generic_msg.warning(msg)

        if status_code:
            msg = ('Looks like the setup had some issues. We are '
                   'gonna go ahead and continue on. Note the error '
                   'messages though.')
            generic_msg.warning(msg)

        return True

    def handle_git_clone(self, location, clone_subdir):
        """Handles cloning of our git repositories.

        Args:
            location (str): The git url we're passing in.
            clone_subdir (str): Where we're pulling the data to.

        Returns:
            int. Subprocess return code.

        """
        clone_dir = os.path.join(self.vim_dir, clone_subdir)
        cmd = ['git', 'clone', location]
        result = 0
        cmd_result = subprocess.Popen(cmd, cwd=clone_dir)
        cmd_result.communicate()
        result = cmd_result.returncode

        return result

    def handle_curl_clone(self, location, clone_subdir):
        """Handles cloning via curl.

        Args:
            location (str): The url we're passing in.
            clone_subdir (str): Where we're pulling the data to.

        Returns:
            str. Returns a string

        """
        clone_dir = os.path.join(self.vim_dir, clone_subdir)
        out_file = os.path.join(clone_dir, location.split('/')[-1])
        cmd = ['curl', '-Sso', out_file, location]
        result = 0
        cmd_result = subprocess.Popen(cmd)
        cmd_result.communicate()
        result = cmd_result.returncode

        return result

    def handle_cleanup(self):
        """Handles the cleanup of files and directories.

        Args:
            self

        Returns:
            int. Status code (anything over 0 is a failure).

        """
        status_code = 0
        cleanup_extensions = [
            '.rst',
            '.markdown',
            '.md'
        ]
        for root, dirs, files in os.walk(self.vim_dir):
            for fname in files:
                ext = os.path.splitext(fname)[-1]
                if ext in cleanup_extensions:
                    full_path = os.path.join(root, fname)
                    try:
                        os.remove(full_path)
                    except OSError as err:
                        msg = ('Error removing file: %s. '
                               'Error: %s' % (full_path, err))
                        generic_msg.warning(msg)
                        status_code += 1

        return status_code

    def handle_mkdir(self, dir_name):
        """Handles making directories so we don't replicate code.

        Args:
            dir_name (str): The directory to create.

        Returns:
            dict. Failure or Success and the output message.
                {'success': True,
                'msg': 'Success message'}
                {'success': False,
                'msg': 'Failure message'}

        """
        out_data = {
            'success': True,
            'msg': 'Successfully created directory: %s' % (dir_name)
        }
        if os.path.exists(dir_name):
            msg = ('Directory %s exists. Attempting to '
                   'remove it.' % (dir_name))
            generic_msg.info(msg)
            rmdir_result = self.handle_rmdir(dir_name)
            if not rmdir_result:
                msg = ('Was not able to delete it. Will continue on '
                       'hoping for the best. :)')
                generic_msg.warning(msg)
                return out_data
        try:
            os.mkdir(dir_name)
        except OSError as err:
            out_data['msg'] = ('Failed to create directory: %s. '
                               'Error: %s' % (dir_name, err))
            out_data['success'] = False

        return out_data

    def handle_rmdir(self, dir_name, recursive=False):
        """Handles removing directories so we don't replicate code.

        Args:
            dir_name (str): The directory to remove.
            recursive (bool): Remove it recursively or not.

        Returns:
            bool. True or False.

        """
        if recursive:
            try:
                os.removedirs(dir_name)
            except OSError as err:
                msg = ('Failure to remove directory %s. '
                       'Error: %s' % (dir_name, err))
                generic_msg.error(msg)
                return False
        else:
            try:
                os.rmdir(dir_name)
            except OSError as err:
                msg = ('Failure to remove directory %s. '
                       'Error: %s' % (dir_name, err))
                generic_msg.error(msg)
                return False

        return True

    def handle_moving_dirs(self, dir_location, new_location):
        """Handles moving our directories.

        Args:
            dir_location (str): The directory to move.
            new_location (str): Where to move it to.

        Returns:
            bool. True or False.

        """
        if os.path.exists(new_location):
            msg = ('Location we are trying to move to already '
                   'exists: %s.' % (new_location))
            generic_msg.error(msg)
            return False

        if os.path.exists(dir_location):
            try:
                shutil.move(dir_location, new_location)
            except shutil.Error as err:
                msg = ('There was an error moving directory %s to %s. '
                       'Error: %s' % (dir_location, new_location, err))
                generic_msg.error(msg)
                return False

        return True

    def handle_failure(self):
        """Handles our failure cases.

        Args:
            None.

        Returns:
            None.

        """
        msg = ('Failed during vim setup. Do you wish to '
               'roll back the changes? [y/n]')
        generic_msg.prompt(msg)
        input_result = raw_input().lower()
        if input_result in self.yes_answers:
            msg = ('Rolling back changes.')
            generic_msg.info(msg)
            rmdir_result = self.handle_rmdir(self.vim_dir, recursive=True)
            if not rmdir_result:
                msg = ('There was an issue removing the .vim directory.')
                generic_msg.error(msg)
            else:
                msg = ('Moving the backup directory %s back '
                       'to .vim.' % (self.backup_directory))
                generic_msg.info(msg)
                result = self.handle_moving_dirs(self.backup_directory,
                                                 self.vim_dir)
        else:
            msg = ('Not rolling back. VIM setup may be '
                   'incomplete. Your backup can be found '
                   'here: %s' % (self.backup_directory))
            generic_msg.warning(msg)

        exit_msg = ('Failed to do the setup properly. My apologies.')
        sys.exit(exit_msg)

if __name__ == '__main__':
    main()
