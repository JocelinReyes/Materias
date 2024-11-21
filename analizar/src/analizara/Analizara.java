/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package analizara;

import java.io.File;

/**
 *
 * @author Jocelin
 */
public class Analizara {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
       
        String path = "C:/Users/Jocelin/Documents/NetBeansProjects/analizara//src/analizara/lexer.flex";
        generar(path);
    }
    public static void generar(String path){
        File file = new File(path);
        JFlex.Main.generate(file);
    }
}
