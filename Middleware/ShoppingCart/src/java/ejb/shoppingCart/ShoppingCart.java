/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ejb.shoppingCart;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;
import javax.annotation.PostConstruct;
import javax.ejb.Stateful;
import javax.ejb.StatefulTimeout;
import javax.enterprise.context.SessionScoped;

/**
 *
 * @author Entropy
 */
@Stateful
@SessionScoped
@StatefulTimeout(unit = TimeUnit.SECONDS, value = 10)
public class ShoppingCart implements IShoppingCart, Serializable {
    private List<Item> items;

    @PostConstruct
    private void initBean() {
        items = new ArrayList<>();
    }

    @Override
    public boolean addProduct(String productID, int quantity) {
        Item item = ItemDB.getInstance().getItem(productID);
        if (item == null) {
            return false;
        }
        for (int i = 0; i < quantity; ++i) {
            items.add(item);
        }
        for (int i = 0; i < items.size(); ++i) {
            System.out.print(items.get(i) + " ");
        }
        System.out.println();
        return true;
    }

    @Override
    public boolean addProduct(String productID) {
        return this.addProduct(productID, 1);
    }

    @Override
    public int removeProduct(String productID, int quantity) {
        int deleteCount = 0;
        for(int i = 0; i < quantity; ++i)
        {
            for(int j = 0; j < items.size(); ++j)
            {
                if(items.get(j).getID().equals(productID))
                {
                    ++deleteCount;
                    items.remove(j);
                    break;
                }
            }
        }
        return deleteCount;
    }

    @Override
    public int removeProduct(String productID) {
        return this.removeProduct(productID, 1);
    }

    @Override
    public double checkout() {
        double total = 0;
        for (int i = 0; i < items.size(); ++i) {
            total += items.get(i).getPrice();
        }
        return total;
    }
    
    @Override
    public String[] getItems()
    {
        String[] ret = new String[items.size()];
        for(int i = 0; i < items.size(); ++i)
        {
            ret[i] = items.get(i).toString();
        }
        return ret;
    }
}
