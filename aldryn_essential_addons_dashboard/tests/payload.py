PAYLOAD = """{
  "id": 56314021,
  "repository": {
    "id": 3861110,
    "name": "aldryn-newsblog",
    "owner_name": "aldryn",
    "url": ""
  },
  "number": "332",
  "config": {
    "language": "python",
    "sudo": false,
    "python": [
      2.6,
      2.7,
      3.3,
      3.4
    ],
    "env": [
      "DJANGO=1.6 CMD=./test",
      "DJANGO=1.7 CMD=./test"
    ],
    "matrix": {
      "allow_failures": [
        {
          "python": 3.3
        },
        {
          "python": 3.4
        },
        {
          "env": "DJANGO=1.7 CMD=./test"
        },
        {
          "env": "DJANGO=1.7 CMD=\\\"flake8 aldryn_newsblog\\\""
        }
      ],
      "exclude": [
        {
          "python": 2.6,
          "env": "DJANGO=1.7 CMD=./test"
        }
      ],
      "fast_finish": true,
      "include": [
        {
          "python": 2.7,
          "env": "DJANGO=1.7 CMD=\\\"flake8 aldryn_newsblog\\\""
        }
      ]
    },
    "cache": {
      "directories": [
        "$HOME/.wheelhouse"
      ]
    },
    "install": [
      "pip install coveralls",
      "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
    ],
    "script": "coverage run test_settings.py",
    "after_success": "coveralls",
    "notifications": {
      "webhooks": "http://example.com/"
    },
    ".result": "configured",
    "os": "linux"
  },
  "status": 0,
  "result": 0,
  "status_message": "Passed",
  "result_message": "Passed",
  "started_at": "2015-03-29T17:00:09Z",
  "finished_at": "2015-03-29T17:02:58Z",
  "duration": 1150,
  "build_url": "https://travis-ci.org/aldryn/aldryn-newsblog/builds/56314021",
  "commit_id": 16142479,
  "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
  "base_commit": "d385c1e49c3d295d9312bf179f7a795914296660",
  "head_commit": "0b28cb2610049c0d5d5c98dd604478dc132d745e",
  "branch": "master",
  "message": "Misc code style cleanups",
  "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
  "committed_at": "2015-03-29T16:19:39Z",
  "author_name": "mikek",
  "author_email": "mike@example.com",
  "committer_name": "mikek",
  "committer_email": "mike@example.com",
  "matrix": [
    {
      "id": 56314022,
      "repository_id": 3861110,
      "parent_id": 56314021,
      "number": "332.1",
      "state": "finished",
      "config": {
        "language": "python",
        "sudo": false,
        "python": 2.6,
        "env": "DJANGO=1.6 CMD=./test",
        "cache": {
          "directories": [
            "$HOME/.wheelhouse"
          ]
        },
        "install": [
          "pip install coveralls",
          "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
        ],
        "script": "coverage run test_settings.py",
        "after_success": "coveralls",
        "notifications": {
          "webhooks": "http://example.com/"
        },
        ".result": "configured",
        "os": "linux"
      },
      "status": 0,
      "result": 0,
      "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
      "branch": "master",
      "message": "Misc code style cleanups",
      "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
      "committed_at": "2015-03-29T16:19:39Z",
      "author_name": "mikek",
      "author_email": "mike@example.com",
      "committer_name": "mikek",
      "committer_email": "mike@example.com",
      "allow_failure": false,
      "finished_at": "2015-03-29T16:55:15Z"
    },
    {
      "id": 56314024,
      "repository_id": 3861110,
      "parent_id": 56314021,
      "number": "332.2",
      "state": "finished",
      "config": {
        "language": "python",
        "sudo": false,
        "python": 2.7,
        "env": "DJANGO=1.6 CMD=./test",
        "cache": {
          "directories": [
            "$HOME/.wheelhouse"
          ]
        },
        "install": [
          "pip install coveralls",
          "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
        ],
        "script": "coverage run test_settings.py",
        "after_success": "coveralls",
        "notifications": {
          "webhooks": "http://example.com/"
        },
        ".result": "configured",
        "os": "linux"
      },
      "status": 0,
      "result": 0,
      "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
      "branch": "master",
      "message": "Misc code style cleanups",
      "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
      "committed_at": "2015-03-29T16:19:39Z",
      "author_name": "mikek",
      "author_email": "mike@example.com",
      "committer_name": "mikek",
      "committer_email": "mike@example.com",
      "allow_failure": false,
      "finished_at": "2015-03-29T17:02:58Z"
    },
    {
      "id": 56314025,
      "repository_id": 3861110,
      "parent_id": 56314021,
      "number": "332.3",
      "state": "finished",
      "config": {
        "language": "python",
        "sudo": false,
        "python": 2.7,
        "env": "DJANGO=1.7 CMD=./test",
        "cache": {
          "directories": [
            "$HOME/.wheelhouse"
          ]
        },
        "install": [
          "pip install coveralls",
          "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
        ],
        "script": "coverage run test_settings.py",
        "after_success": "coveralls",
        "notifications": {
          "webhooks": "http://example.com/"
        },
        ".result": "configured",
        "os": "linux"
      },
      "status": 1,
      "result": 1,
      "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
      "branch": "master",
      "message": "Misc code style cleanups",
      "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
      "committed_at": "2015-03-29T16:19:39Z",
      "author_name": "mikek",
      "author_email": "mike@example.com",
      "committer_name": "mikek",
      "committer_email": "mike@example.com",
      "allow_failure": true,
      "finished_at": "2015-03-29T16:54:41Z"
    },
    {
      "id": 56314026,
      "repository_id": 3861110,
      "parent_id": 56314021,
      "number": "332.4",
      "state": "finished",
      "config": {
        "language": "python",
        "sudo": false,
        "python": 3.3,
        "env": "DJANGO=1.6 CMD=./test",
        "cache": {
          "directories": [
            "$HOME/.wheelhouse"
          ]
        },
        "install": [
          "pip install coveralls",
          "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
        ],
        "script": "coverage run test_settings.py",
        "after_success": "coveralls",
        "notifications": {
          "webhooks": "http://example.com/"
        },
        ".result": "configured",
        "os": "linux"
      },
      "status": 1,
      "result": 1,
      "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
      "branch": "master",
      "message": "Misc code style cleanups",
      "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
      "committed_at": "2015-03-29T16:19:39Z",
      "author_name": "mikek",
      "author_email": "mike@example.com",
      "committer_name": "mikek",
      "committer_email": "mike@example.com",
      "allow_failure": true,
      "finished_at": "2015-03-29T16:53:08Z"
    },
    {
      "id": 56314027,
      "repository_id": 3861110,
      "parent_id": 56314021,
      "number": "332.5",
      "state": "finished",
      "config": {
        "language": "python",
        "sudo": false,
        "python": 3.3,
        "env": "DJANGO=1.7 CMD=./test",
        "cache": {
          "directories": [
            "$HOME/.wheelhouse"
          ]
        },
        "install": [
          "pip install coveralls",
          "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
        ],
        "script": "coverage run test_settings.py",
        "after_success": "coveralls",
        "notifications": {
          "webhooks": "http://example.com/"
        },
        ".result": "configured",
        "os": "linux"
      },
      "status": 1,
      "result": 1,
      "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
      "branch": "master",
      "message": "Misc code style cleanups",
      "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
      "committed_at": "2015-03-29T16:19:39Z",
      "author_name": "mikek",
      "author_email": "mike@example.com",
      "committer_name": "mikek",
      "committer_email": "mike@example.com",
      "allow_failure": true,
      "finished_at": "2015-03-29T16:53:12Z"
    },
    {
      "id": 56314029,
      "repository_id": 3861110,
      "parent_id": 56314021,
      "number": "332.6",
      "state": "finished",
      "config": {
        "language": "python",
        "sudo": false,
        "python": 3.4,
        "env": "DJANGO=1.6 CMD=./test",
        "cache": {
          "directories": [
            "$HOME/.wheelhouse"
          ]
        },
        "install": [
          "pip install coveralls",
          "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
        ],
        "script": "coverage run test_settings.py",
        "after_success": "coveralls",
        "notifications": {
          "webhooks": "http://example.com/"
        },
        ".result": "configured",
        "os": "linux"
      },
      "status": 1,
      "result": 1,
      "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
      "branch": "master",
      "message": "Misc code style cleanups",
      "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
      "committed_at": "2015-03-29T16:19:39Z",
      "author_name": "mikek",
      "author_email": "mike@example.com",
      "committer_name": "mikek",
      "committer_email": "mike@example.com",
      "allow_failure": true,
      "finished_at": "2015-03-29T16:58:39Z"
    },
    {
      "id": 56314030,
      "repository_id": 3861110,
      "parent_id": 56314021,
      "number": "332.7",
      "state": "finished",
      "config": {
        "language": "python",
        "sudo": false,
        "python": 3.4,
        "env": "DJANGO=1.7 CMD=./test",
        "cache": {
          "directories": [
            "$HOME/.wheelhouse"
          ]
        },
        "install": [
          "pip install coveralls",
          "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
        ],
        "script": "coverage run test_settings.py",
        "after_success": "coveralls",
        "notifications": {
          "webhooks": "http://example.com/"
        },
        ".result": "configured",
        "os": "linux"
      },
      "status": 1,
      "result": 1,
      "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
      "branch": "master",
      "message": "Misc code style cleanups",
      "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
      "committed_at": "2015-03-29T16:19:39Z",
      "author_name": "mikek",
      "author_email": "mike@example.com",
      "committer_name": "mikek",
      "committer_email": "mike@example.com",
      "allow_failure": true,
      "finished_at": "2015-03-29T16:53:45Z"
    },
    {
      "id": 56314031,
      "repository_id": 3861110,
      "parent_id": 56314021,
      "number": "332.8",
      "state": "finished",
      "config": {
        "language": "python",
        "sudo": false,
        "python": 2.7,
        "env": "DJANGO=1.7 CMD=\\\"flake8 aldryn_newsblog\\\"",
        "cache": {
          "directories": [
            "$HOME/.wheelhouse"
          ]
        },
        "install": [
          "pip install coveralls",
          "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
        ],
        "script": "coverage run test_settings.py",
        "after_success": "coveralls",
        "notifications": {
          "webhooks": "http://example.com/"
        },
        ".result": "configured",
        "os": "linux"
      },
      "status": 1,
      "result": 1,
      "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
      "branch": "master",
      "message": "Misc code style cleanups",
      "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
      "committed_at": "2015-03-29T16:19:39Z",
      "author_name": "mikek",
      "author_email": "mike@example.com",
      "committer_name": "mikek",
      "committer_email": "mike@example.com",
      "allow_failure": true,
      "finished_at": "2015-03-29T16:59:08Z"
    },
    {
      "id": 56314032,
      "repository_id": 3861110,
      "parent_id": 56314021,
      "number": "332.8",
      "state": "finished",
      "config": {
        "language": "python",
        "sudo": false,
        "python": 3.5,
        "env": "DJANGO=1.9",
        "cache": {
          "directories": [
            "$HOME/.wheelhouse"
          ]
        },
        "install": [
          "pip install coveralls",
          "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
        ],
        "script": "coverage run test_settings.py",
        "after_success": "coveralls",
        "notifications": {
          "webhooks": "http://example.com/"
        },
        ".result": "configured",
        "os": "linux"
      },
      "status": 0,
      "result": 0,
      "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
      "branch": "master",
      "message": "Misc code style cleanups",
      "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
      "committed_at": "2015-03-29T16:19:39Z",
      "author_name": "mikek",
      "author_email": "mike@example.com",
      "committer_name": "mikek",
      "committer_email": "mike@example.com",
      "allow_failure": true,
      "finished_at": "2015-03-29T16:59:08Z"
    },

    {
      "id": 56314033,
      "repository_id": 3861110,
      "parent_id": 56314021,
      "number": "332.8",
      "state": "finished",
      "config": {
        "language": "python",
        "sudo": false,
        "env": "DJANGO=1.9",
        "cache": {
          "directories": [
            "$HOME/.wheelhouse"
          ]
        },
        "install": [
          "pip install coveralls",
          "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
        ],
        "script": "coverage run test_settings.py",
        "after_success": "coveralls",
        "notifications": {
          "webhooks": "http://example.com/"
        },
        ".result": "configured",
        "os": "linux"
      },
      "status": 0,
      "result": 0,
      "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
      "branch": "master",
      "message": "Misc code style cleanups",
      "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
      "committed_at": "2015-03-29T16:19:39Z",
      "author_name": "mikek",
      "author_email": "mike@example.com",
      "committer_name": "mikek",
      "committer_email": "mike@example.com",
      "allow_failure": true,
      "finished_at": "2015-03-29T16:59:08Z"
    },
    {
      "id": 56314033,
      "repository_id": 3861110,
      "parent_id": 56314021,
      "number": "332.8",
      "state": "finished",
      "config": {
        "language": "python",
        "sudo": false,
        "python": 3.5,
        "cache": {
          "directories": [
            "$HOME/.wheelhouse"
          ]
        },
        "install": [
          "pip install coveralls",
          "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
        ],
        "script": "coverage run test_settings.py",
        "after_success": "coveralls",
        "notifications": {
          "webhooks": "http://example.com/"
        },
        ".result": "configured",
        "os": "linux"
      },
      "status": 0,
      "result": 0,
      "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
      "branch": "master",
      "message": "Misc code style cleanups",
      "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
      "committed_at": "2015-03-29T16:19:39Z",
      "author_name": "mikek",
      "author_email": "mike@example.com",
      "committer_name": "mikek",
      "committer_email": "mike@example.com",
      "allow_failure": true,
      "finished_at": "2015-03-29T16:59:08Z"
    }
  ],
  "type": "pull_request",
  "state": "passed",
  "pull_request": true,
  "pull_request_number": 150,
  "pull_request_title": "Take published state into account in custom manager methods",
  "tag": null
}"""

FAILING_PAYLOAD = """{
  "id": 56314021,
  "repository": {
    "id": 3861110,
    "name": "aldryn-newsblog",
    "owner_name": "aldryn",
    "url": ""
  },
  "number": "332",
  "config": {
    "language": "python",
    "sudo": false,
    "python": [
      2.6,
      2.7,
      3.3,
      3.4
    ],
    "env": [
      "DJANGO=1.6 CMD=./test",
      "DJANGO=1.7 CMD=./test"
    ],
    "matrix": {
      "allow_failures": [
        {
          "python": 3.3
        },
        {
          "python": 3.4
        },
        {
          "env": "DJANGO=1.7 CMD=./test"
        },
        {
          "env": "DJANGO=1.7 CMD=\\\"flake8 aldryn_newsblog\\\""
        }
      ],
      "exclude": [
        {
          "python": 2.6,
          "env": "DJANGO=1.7 CMD=./test"
        }
      ],
      "fast_finish": true,
      "include": [
        {
          "python": 2.7,
          "env": "DJANGO=1.7 CMD=\\\"flake8 aldryn_newsblog\\\""
        }
      ]
    },
    "cache": {
      "directories": [
        "$HOME/.wheelhouse"
      ]
    },
    "install": [
      "pip install coveralls",
      "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
    ],
    "script": "coverage run test_settings.py",
    "after_success": "coveralls",
    "notifications": {
      "webhooks": "http://example.com/"
    },
    ".result": "configured",
    "os": "linux"
  },
  "status": 1,
  "result": 0,
  "status_message": "Passed",
  "result_message": "Passed",
  "started_at": "2015-03-29T17:00:09Z",
  "finished_at": "2015-03-29T17:02:58Z",
  "duration": 1150,
  "build_url": "https://travis-ci.org/aldryn/aldryn-newsblog/builds/56314021",
  "commit_id": 16142479,
  "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
  "base_commit": "d385c1e49c3d295d9312bf179f7a795914296660",
  "head_commit": "0b28cb2610049c0d5d5c98dd604478dc132d745e",
  "branch": "master",
  "message": "Misc code style cleanups",
  "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
  "committed_at": "2015-03-29T16:19:39Z",
  "author_name": "mikek",
  "author_email": "mike@example.com",
  "committer_name": "mikek",
  "committer_email": "mike@example.com",
  "matrix": [
    {
      "id": 56314022,
      "repository_id": 3861110,
      "parent_id": 56314021,
      "number": "332.1",
      "state": "finished",
      "config": {
        "language": "python",
        "sudo": false,
        "python": 2.6,
        "env": "DJANGO=1.6 CMD=./test",
        "cache": {
          "directories": [
            "$HOME/.wheelhouse"
          ]
        },
        "install": [
          "pip install coveralls",
          "pip install -r \\\"test_requirements/django-$DJANGO.txt\\\""
        ],
        "script": "coverage run test_settings.py",
        "after_success": "coveralls",
        "notifications": {
          "webhooks": "http://example.com/"
        },
        ".result": "configured",
        "os": "linux"
      },
      "status": 0,
      "result": 0,
      "commit": "0954ef00b9f9422a184e35d87815640f489bbe05",
      "branch": "master",
      "message": "Misc code style cleanups",
      "compare_url": "https://github.com/aldryn/aldryn-newsblog/pull/150",
      "committed_at": "2015-03-29T16:19:39Z",
      "author_name": "mikek",
      "author_email": "mike@example.com",
      "committer_name": "mikek",
      "committer_email": "mike@example.com",
      "allow_failure": false,
      "finished_at": "2015-03-29T16:55:15Z"
    }
  ],
  "type": "pull_request",
  "state": "passed",
  "pull_request": true,
  "pull_request_number": 150,
  "pull_request_title": "Take published state into account in custom manager methods",
  "tag": null
}"""
