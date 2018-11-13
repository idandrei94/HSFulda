/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package beans;

import javax.ejb.Stateless;

/**
 *
 * @author Entropy
 */
@Stateless
public class BMIBean {
    public double calcBMI(double height, double weight)
    {
        return weight / (height * height);
    }
}
