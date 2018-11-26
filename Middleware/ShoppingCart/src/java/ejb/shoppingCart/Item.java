/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ejb.shoppingCart;

/**
 *
 * @author Entropy
 */
public class Item {
    private String _ID;
    private String _name;
    private double _price;
    
    public Item(String ID, String name, double price)
    {
        this._ID = ID;
        this._name = name;
        this._price = price;
    }
    
    public String getID()
    {
        return _ID;
    }
    
    public String getName()
    {
        return _name;
    }
    
    public double getPrice()
    {
        return _price;
    }
    
    public String toString()
    {
        return _ID+" "+_name+" "+_price+" EUR";
    }
}
