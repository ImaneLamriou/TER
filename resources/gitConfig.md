## Add these servers to your Git (as remote adress):
	- This is our main git repository: https://github.com/ImaneLamriou/TER.git
	- `git remote add origin https://github.com/ImaneLamriou/TER.git`: This command is to add main git repository of our project to pull from.
	- `git remote -v`: This command is to verify all remote servers

## Don't forget:
To do this command every time that you'll work on the project:
	- `git pull origin master`

## To add files on the GitHub:
Do these commands step by step:
- See all files and folders that are changed:
´git status´
- Edit the file .gitignore to remove unnecessary files.
- Add files to the stage:
´git add FILENAME_TO_ADD´
- Write a comprehensive message and commit:
´git commit -m 'A comprehensive message about the job that you did in present tense and in English'´
-  Send your commits to "hub" or any address that you gave for your remote:
´git push hub YOUR_BRANCHE_NAME´
- Go on your GitHub repository online to verify if you can see your new commits or not!
