/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ejb.Shopping;

import ejb.shoppingCart.IShoppingCart;
import java.io.IOException;
import java.io.PrintWriter;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 *
 * @author Entropy
 */
@WebServlet(name = "ShoppingServlet", urlPatterns = {"/shopping"})
public class ShoppingServlet extends HttpServlet {

    private static final long serialVersionUID = 6L;
    private static final String CART_SESSION_KEY = "shoppingCart";

    /**
     * Processes requests for both HTTP <code>GET</code> and <code>POST</code>
     * methods.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        System.out.println("Hello from servlet");
        IShoppingCart cartBean = (IShoppingCart) request.getSession().getAttribute(CART_SESSION_KEY);
        
        if (cartBean == null || !request.isRequestedSessionIdValid()) {
            System.out.println("bad session");
            // first time, session doesn't exist
            try {
                InitialContext ic = new InitialContext();
                cartBean = (IShoppingCart) ic.lookup("java:global/ShoppingCart/ShoppingCart");
                request.getSession().setAttribute(CART_SESSION_KEY, cartBean);
                request.getSession().setMaxInactiveInterval(4);
                System.out.println("ShoppingCart created");
            } catch (NamingException e) {
                System.out.println("Error getting session");
            }
        }
        String ID = request.getParameter("ID");
        cartBean.addProduct(ID);
        System.out.println("Total: " + cartBean.checkout());
        response.setContentType("text/plain;charset=UTF-8");
        String items[] = cartBean.getItems();
        cartBean = null;
        for (int i = 0; i < items.length; ++i) {
            try (PrintWriter out = response.getWriter()) {
                out.print(items[i]);
            }
        }
    }
// <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">

    /**
     * Handles the HTTP <code>GET</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Handles the HTTP <code>POST</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Short description";
    }// </editor-fold>

}
