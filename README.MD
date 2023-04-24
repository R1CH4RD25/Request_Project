# TRANSPORTATION REQUEST APP

# Testing Setup

Please use the following steps to setup the application:

* **Setup the Virtual Environment**
    * Using the terminal, create a virtual environment in a folder of your choosing.
    * After creation, **install requirements.txt**
    * Example:
        ``` powershell
        # create venv folder and virtual environment
        python -m venv .venv

        # activate virtual environment
        .\.venv\Scripts\activate

        # install Flask
        pip install -r .\requirements.txt

        # traverse to src folder and install custom path module
        cd .\src\
        pip install -e .
        ```


# Run Tests for Test Driven Development Application Model

Please use the following steps to test the application:

* **Open Terminal and Run Test Commands**
    * Activate the **virtual environment**
        ``` powershell
        # activate virtual environment
        .\.venv\Scripts\activate
        ```
    * Run pytest commands using python
        ``` powershell
        # Unit Tests
        pytest .\tests\unit\test_assign.py
        pytest .\tests\unit\test_services.py

        # Integration Test
        pytest .\tests\integration\test_orm.py
        pytest .\tests\integration\test_repository.py
        pytest .\tests\integration\test_uow.py

        # End-to-End Test
        pytest .\tests\e2e\test_api.py  
        ```

    * Run ALL tests at once using pytest
        ``` powershell
        # All Tests
        pytest .\tests\
        ```