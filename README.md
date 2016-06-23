#Trans *.json to *.protoc

##How to use
	
1. Put *.json files in dir "json_file",

2. run "python json_to_protoc.py"

3. Get *.protoc files in dir "protoc_file"

##Example
Input

	{
	    "kind": "person",
	    "fullName": "John Doe",
	    "age": 22,
	    "gender": "Male",
	    "phoneNumber": {
	        "areaCode": "206",
	        "number": "1234567"
	    },
	    "children": [
	        {
	            "name": "Jane",
	            "gender": "Female",
	            "age": "6"
	        },
	        {
	            "name": "John",
	            "gender": "Male",
	            "age": "15"
	        }
	    ],
	    "citiesLived": [
	        {
	            "place": "Seattle",
	            "yearsLived": [
	                "1995"
	            ]
	        },
	        {
	            "place": "Stockholm",
	            "yearsLived": [
	                "2005"
	            ]
	        }
	    ]
	}
	
Output

	message PersonData {
	  required string kind = 1;
	  required string gender = 2;
	  required int64 age = 3;
	  repeated CitiesLived citiesLived = 4;
	  required PhoneNumber phoneNumber = 5;
	  required string fullName = 6;
	  repeated Children children = 7;
	}
	
	message Children {
	  required string gender = 1;
	  required string age = 2;
	  required string name = 3;
	}
	
	message PhoneNumber {
	  required string areaCode = 1;
	  required string number = 2;
	}
	
	message CitiesLived {
	  repeated string yearsLived = 1;
	  required string place = 2;
	}