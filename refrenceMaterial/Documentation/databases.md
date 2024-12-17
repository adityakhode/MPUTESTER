# Database code Documentation

## Libraries Used
- ```
  pandas   # For reading the  Exel file (.xlxs)
  sqlite3  # For Handling Database
  openpyxl # For Handling file Manager and external files.
  ```
- sqlite3 : It is specially used because it doesn't requires the database instance running and no password requires no much more setup for `SQL`.
- Can Directly run SQL commands using builtin Function.

## Classes inside database file
1. **UnitMaster**
- This class has all the paramaters related to the MPU sensor.
2. **PartyMaster**
- This class has all the paramaters related to the *Twintech Control System* customers.
3. **ResultMaster**
- This class has all the paramaters related to the MPU sensor test result.
- It takes all the clients <strong>Supplier code</strong> & <strong>Client name</strong> from partyMaster and make seperate database for each of them.

## Common functions in all the classes
1. **create()**
- This function has no paramaters and it creates the table with the paramaters that has defined in class.
- If the table is created then it won't create.
- It is used in such places where there is not required, for example in getting some paramater we called `create()` at very first line because it ensures the table is present and handles the program from crashing.
- To call the function
- ```
  UnitMaster.create()  # the table will be created if not exist.
  PartyMaster.create()
  ResultMaster.create(tableName)
  ```
2. **insert(params)**
- This function does the work of inserting the data row by row.
- we feed some paramaters accourding to tables and it inserts the data.
- To call the function
- ```
  UnitMaster.insert(*param)  # the function will insert the data into the respective table.
  PartyMaster.insert(*param) # paramater length differs accourding to the coloums.
  ResultMaster.insert(tableName, *param)
  ```
  
## Common Function in `UnitMaster` and `partyMaster`
1. **addData(filename)**
- This function does the work of importing from exel and saving it to databases.
- This simplifies the normal workes to import the data to database.
- To call the function
- ```
  UnitMaster.addData(filename)  # the function will insert the data from exel file .xlxs into the respective table.
  PartyMaster.addData(filename)
  ```
2. **dataAvailable()**
- This will ensure is the data present in database or not, basically it checks if rows are less than 1.
- As we impleented `create()` function to hanldle data and initially we want to instruct the user to add the data files.
- To call the function
- ```
  UnitMaster.dataAvailable()  # the function will check if rows < 1 and return true or false
  PartyMaster.dataAvailable()
  ```

## Individual function
1.**unitMaster**
- `getPartNo` : This function checks if the part Number exixt and returns the boolean output.
- To call the function
- ```
  untimaster.getPartNo(PartNo)
  ```
- `getPartName(PartNo)` : It returns the <strong>partName</strong> by giving part number.
- To call the function
- ```
  untimaster.getPartName(PartNo)
  ```
- `getaPartNoList()` : It returns all the part number.
- To call the function
- ```
  untimaster.getaPartNoList()
  ```

2. **partyMaster**
- `getSupplierCodeAndNameList()` : It return the supplier code and Client Name List.
- It is use in createAll() function in `resultMaster` table, so it could create a independent database for different clients.
- To call the function
- ```
  partyMaster.getSupplierCodeAndNameList()
  ```

3. **resultMaster**
- `getDetails(tablename, TcNo)` : returns all the datails of that Test Certificate number of particular customer.
- To call the function
- ```
  resultMaster.getDetails(tablename, TcNo)
  ```
