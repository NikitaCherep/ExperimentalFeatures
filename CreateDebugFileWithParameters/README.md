# Creating debug file with parameters

This function creates a debug file based on ```parameters.json``` that contains the parameters to be changed.

# Guide

1. Run script
2. Run App

# Supported parameters

| № | Field           | Type    | Sample          |
|---|-----------------|---------|-----------------|
| 1 | loggingEnabled  | Boolean | true            |
| 2 | testMode        | Boolean | true            |
| 3 | endpoint        | String  | http://test.com |
| 4 | coppa           | Boolean | true            |
| 5 | usPrivacyString | String  | 1Y--            |
| 6 | subjectToGDPR   | Boolean | true            |
| 7 | consent         | Boolean | true            |
| 8 | GDPRString      | String  | sEmgrqRfQtjew5k |

Sample:

```json
{
  "testMode": true,
  "loggingEnabled": true,
  "endpoint": "http://test.com",
  "coppa": true,
  "usPrivacyString": "1Y--",
  "subjectToGDPR": true,
  "consent": true,
  "GDPRString": "sEmgrqRfQtjew5k"
}
```

# Command

### Push debug file

```commandline
python3 'path_to_runnable' 'application_package'
```

Sample:

```commandline
python3 script/runnable.py io.bidmachine.test.app
```

### Remove debug file

```commandline
python3 'path_to_runnable' 'application_package' --clear
```

Sample:

```commandline
python3 script/runnable.py io.bidmachine.test.app  --clear
```

# Help

For more information use:

```commandline
python3 'path_to_runnable' --help
```

Sample:

```commandline
python3 script/runnable.py --help
```