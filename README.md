<!-- Project Bio -->

<div align="center">
    <h1>ToDo Backend GraphQL</h1>
    <p>
        My first project that uses GQL <br />
        <a href="#"><strong>Explore the docs »</strong></a>
        <br/>
        <br/>
        <a href="https://todo-graphql-backend.vercel.app/">View demo</a>
        ·
        <a href="https://github.com/SoSaymon/todo-graphql-backend/issues">Report Bug</a>
        ·
        <a href="https://github.com/SoSaymon/todo-graphql-backend/issues">Request Feature</a>
    </p>
</div>

<!-- Table of Contents -->

<details>
    <summary>Table of Contents</summary>
    <ol>
        <li>
            <a href="#about-the-project">About The Project</a>
            <ul>
                <li><a href="#built-with">Built With</a></li>
            </ul>
        </li>
        <li>
            <a href="#getting-started">Getting Started</a>
            <ul>
                <li><a href="#prerequisites">Prerequisites</a></li>
                <li><a href="#installation">Installation</a></li>
                <li><a href="#usage">Usage</a></li>
            </ul>
        </li>
        <li><a href="#roadmap">Roadmap</a></li>
        <li><a href="#contributing">Contributing</a></li>
        <li><a href="#license">License</a></li>
    </ol>
</details>

<!-- About the project -->
<span id="about-the-project"></span>
## About The Project

This is my first project that uses GraphQL. This project is a backend for a ToDo application. The project is deployed on [Vercel](https://todo-graphql-backend.vercel.app/), where you can test it using the GraphQL Playground.

<!-- Built with -->
<span id="built-with"></span>
### Built With

* FastAPI
* GraphQL
* SQLAlchemy
* PostgreSQL
* Docker (Work in progress)
* Vercel

<!-- Getting started -->
<span id="getting-started"></span>
## Getting Started

To get a local copy up and running follow these simple steps.

<!-- Prerequisites -->
<span id="prerequisites"></span>
### Prerequisites

* Python 3.12 or higher (But there should be no problems with lower versions)
* Poetry or pipenv
* PostgreSQL (Or any other database supported by SQLAlchemy)
* Caffeine (Optional)
* Fun (Required)

<!-- Installation -->
<span id="installation"></span>
### Installation

1. Clone the repo
    ```sh
    git clone https://github.com/SoSaymon/todo-graphql-backend.git
    ```
2. Install dependencies
    ```sh
    poetry install
    ```
    or
    ```sh
    pip install -r requirements.txt
    ```
3. Create a `.env` file in the root directory and add the following variables:
    ```env
    DB_URL=DATABASE_URL
    SECRET_KEY=JWT_SECRET_KEY
    ALGORITHM=JWT_ALGORITHM
    TOKEN_EXPIRATION_TIME_MINUTES=JWT_TOKEN_EXPIRATION_TIME
    ```
4. Run the project
    ```sh
    uvicorn app.main:app --reload
    ```
   
<!-- Usage -->
<span id="usage"></span>
### Usage

You can find the documentation for the API [here](https://todo-graphql-backend.vercel.app/).

<!-- Roadmap -->
<span id="roadmap"></span>
## Roadmap

See the [open issues](https://github.com/SoSaymon/todo-graphql-backend/issues) for a list of proposed features (and known issues).

<!-- Contributing -->
<span id="contributing"></span>
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request
6. Wait for review
7. Have fun :)

<!-- License -->
<span id="license"></span>
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- Contact -->
<span id="contact"></span>
## Contact

SoSaymon - [Telegram](https://t.me/SoSaymon) - [Email](mailto:szymon.chirowski@protonmail.com)

Project Link: https://github.com/SoSaymon/todo-graphql-backend/



