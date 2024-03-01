# partition_mcnp
scripts for dividing a large mcnp model into components  

'extract_fill_card example.i' - extracts map cells into a separate 'example_fill_card.i' file  
'extract_universes example.i' - extracts each universe into its own file ('ex_u_universes/u123.i')  
'del_material example.i 15' - copies the mcnp model, except for the cells of the specified material ('del_M15_example.i')  
