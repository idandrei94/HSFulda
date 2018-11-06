/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package persistence;

import java.io.Serializable;
import java.util.ArrayList;

/**
 *
 * @author Entropy
 */
public class Data implements Serializable {
    private ArrayList<Entry> entries;
    private static Data _instance = null;
    
    private Data()
    {
        entries = new ArrayList();
    }
    
    public static Data getInstance()
    {
        if(_instance == null)
            _instance = new Data();
        return _instance;
    }
    
    public void Add(Entry entry)
    {
        entries.add(entry);
    }
    
    public int Size()
    {
        return entries.size();
    }
    
    public Entry Get(int index)
    {
        return entries.get(index);
    }
}
