# ORTC
An implementation of Optimal Routing Table Constructor
## Usage
- Create data.txt in the same directory as the program.
- The First line indicates the tag of the next jump of 0.0.0.0 (default route) Setting it to "empty" (this string) means no default route.
- Each of other lines indicates a route. Format: IP Mask_Length Tag_of_Next_Jump
- Every line should ends with a semicolon(;).
- There is an example file data-example.txt.
## Reference
R. P. Draves, C. King, S. Venkatachary and B. D. Zill, "Constructing optimal IP routing tables," IEEE INFOCOM '99. Conference on Computer Communications. Proceedings. Eighteenth Annual Joint Conference of the IEEE Computer and Communications Societies. The Future is Now (Cat. No.99CH36320), 1999, pp. 88-97 vol.1, doi: 10.1109/INFCOM.1999.749256.
