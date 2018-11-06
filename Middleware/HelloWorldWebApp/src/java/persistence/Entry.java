package persistence;


import java.io.Serializable;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Entropy
 */
public class Entry implements Serializable {
    public String _name;
    public String _date;
    public double _height;
    public double _weight;
    
    public Entry(String name, String date, double height, double weight)
    {
        this._name = name;
        this._date = date;
        this._height = height;
        this._weight = weight;
    }
    
    public String Name() { return _name; }
    public String Date() { return _date; }
    public double Height() { return _height; }
    public double Weight() { return _weight; }
}
