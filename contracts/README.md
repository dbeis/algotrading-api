# Contracts
Versioned

## Definition 

Contracts are patterns that form an agreement on how the API is designed. Data flow among components can be hard to keep track or maintained, sometimes forcing us to write print statements everywhere trying to catch malformed data. Contracts help in that way, since they define the data types that flow through the system.


## Usage

`from contracts import *`

or

`from contracts.[versionNumber] import *` to keep compatibility -- update `versionNumber` incrementally to avoid breaking code.

All the changes after publishing are made as additions. 

This package only contains plain-old python classes only used for JSON serialization and deserialization.