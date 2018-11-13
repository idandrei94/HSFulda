/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package bmi;

import beans.BMIBean;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.Arrays;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.sql.*;
import javax.ejb.EJB;

/**
 *
 * @author Entropy
 */
@WebServlet(name = "BMI", urlPatterns = {"/BMI"})
public class BMI extends HttpServlet {

    @EJB
    private BMIBean bMIBean;

    private String name;
    private String date;
    private double height;
    private double weight;

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
        try {
            name = request.getParameter("name");
            date = request.getParameter("currentDate");
            height = Integer.parseInt(request.getParameter("height"));
            weight = Integer.parseInt(request.getParameter("weight"));
            
            
            
            
            double bmi = bMIBean.calcBMI(height, weight);
            response.setContentType("text/plain;charset=UTF-8");
            try (PrintWriter out = response.getWriter()) {
                out.print(bmi);
            }
            Connection conn = getConnection();
            String sql = "CREATE TABLE IF NOT EXISTS bmi (name VARCHAR(30), date VARCHAR(11), height FLOAT, weight FLOAT);";
            Statement stmt = conn.createStatement();
            stmt.execute(sql);
            stmt = conn.createStatement();
            sql = "INSERT INTO bmi VALUES('"+name+"','"+date+"', "+height+","+weight+");"; 
            stmt.execute(sql);
            stmt = conn.createStatement();
            sql = "SELECT * FROM bmi";
            stmt.execute(sql);
            ResultSet res = stmt.executeQuery(sql);
            while(res.next())
            {
                String name = res.getString("name");
                String date = res.getString("date");
                double height = res.getFloat("height");
                double weight = res.getFloat("weight");
                System.out.println("Name " + name);
                System.out.println("Date " + date);
                System.out.println("Height " + height);
                System.out.println("Weight " + weight);
            }
            conn.close();
            
        } catch (Exception ex) {
            response.setContentType("text/json;charset=UTF-8");
            try (PrintWriter out = response.getWriter()) {
                out.println("{ message: \"Invalid request!\"\n exception:" + ex.getMessage() + "\"");
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

    private Connection getConnection() {
        Connection c = null;

        try {
            Class.forName("org.sqlite.JDBC");
            c = DriverManager.getConnection("jdbc:sqlite:test.db");
        } catch (Exception e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
            System.exit(0);
        }
        System.out.println("Opened database successfully");
        return c;
    }

}
