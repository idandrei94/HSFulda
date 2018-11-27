
import static com.sun.org.glassfish.external.amx.AMXUtil.prop;
import ejb.shoppingCart.IShoppingCart;
import java.util.Properties;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 *
 * @author Entropy
 */
public class MainClass {

    public static void main(String args[]) throws InterruptedException {
        IShoppingCart cartBean = null;

        if (cartBean == null) {
            System.out.println("getting the bean");
            try {
                Properties props = new Properties();
                props.setProperty("org.omg.CORBA.ORBInitialHost", "localhost"); // default!
                props.setProperty("org.omg.CORBA.ORBInitialPort", "13790"); // default!
                InitialContext ic = new InitialContext(props);
                System.out.println("Lookup...");
                cartBean = (IShoppingCart) ic.lookup("java:global/ShoppingCart/ShoppingCart");
                System.out.println("Lookup finished");
                System.out.println("ShoppingCart created");
            } catch (NamingException e) {
                System.out.println("Error getting session");
            }
        }
        for (int index = 0; index < 3; ++index) {
            try {
                String ID = index + "";
                cartBean.addProduct(ID);
                System.out.println("Total: " + cartBean.checkout());
                String items[] = cartBean.getItems();
                for (int i = 0; i < items.length; ++i) {
                    System.out.println(items[i]);
                }
            } catch (Exception e) {
                System.out.println("Bean's dead");
            }
            if (index == 1) {
                System.out.println("Sleeping 15 sec");
                Thread.sleep(15000);
            } else {
                System.out.println("Sleeping 1 sec");
                Thread.sleep(1000);
            }
        }
        System.out.println("MainClass.main() finished");
    }
}
