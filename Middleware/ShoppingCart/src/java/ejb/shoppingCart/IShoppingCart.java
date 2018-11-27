/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ejb.shoppingCart;

import javax.ejb.Local;
import javax.ejb.Remote;
import javax.ejb.Stateful;

/**
 *
 * @author Entropy
 */
@Remote
public interface IShoppingCart {

    public boolean addProduct(String productID, int quantity);

    public boolean addProduct(String productID);
    
    public int removeProduct(String productID, int quantity);
    
    public int removeProduct(String productID);
    
    public double checkout();
    
    public String[] getItems();
}
