/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ejb.shoppingCart;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Entropy
 */
public class ItemDB {

    private List<Item> items;
    private static ItemDB instance = null;

    public static ItemDB getInstance()
    {
        if(instance == null)
            instance = new ItemDB();
        return instance;
    }
    
    private ItemDB() {
        items = new ArrayList<>();
        items.add(new Item("0", "Book", 15.99));
        items.add(new Item("1", "Sandwich", 5.99));
        items.add(new Item("2", "Chewing gum", 1.99));
    }

    public Item getItem(String ID) 
    {
        for(int i = 0; i < items.size(); ++i)
        {
            if(items.get(i).getID().equals(ID))
                return items.get(i);
        }
        return null;
    }
}