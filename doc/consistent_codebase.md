# To maintain a consistent codebase:

#### We use pre-commit with Black and Flake8

- Let black format your code. This ensures consistency in styling, including the use of double quotes for strings.
- Run flake8 to catch any potential issues, bugs, or deviations from coding standards.
- Address any issues raised by flake8 that aren't related to code style (since black handles style).
- 
In practice, when you run git commit, the pre-commit tool will run both black and flake8 in the order they appear in your **.pre-commit-config.yaml**. 
If black modifies any files, you'll need to re-add them (git add) before committing. If flake8 raises any issues, you'll need to address them manually before the commit can proceed.


#### Here's the typical flow when using pre-commit hooks:

- You run git commit -m "Your commit message".
- The pre-commit hooks run.
- If a hook like black makes changes, the commit will be paused.
- You stage the changes with git add <modified-files>.
- You finalize the commit with **git commit --continue**.

The git commit --continue command tells Git that you've resolved the issues and that it should proceed with the commit using the message you originally provided.