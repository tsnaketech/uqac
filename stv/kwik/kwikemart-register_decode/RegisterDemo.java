import java.util.ArrayList;
import java.util.List;
import stev.kwikemart.Item;
import stev.kwikemart.PaperRoll;
import stev.kwikemart.Register;
import stev.kwikemart.Upc;

public class RegisterDemo {
   public static void main(String[] args) {
      Register register = Register.getRegister();
      register.changePaper(PaperRoll.SMALL_ROLL);
      List<Item> grocery = new ArrayList();
      grocery.add(new Item(Upc.generateCode("12345678901"), "Bananas", 1.0D, 1.5D));
      grocery.add(new Item(Upc.generateCode("22804918500"), "Beef", 0.5D, 5.75D));
      grocery.add(new Item(Upc.generateCode("12345678901"), "Bananas", -1.0D, 1.5D));
      grocery.add(new Item(Upc.generateCode("64748119599"), "Chewing gum", 2.0D, 0.99D));
      grocery.add(new Item(Upc.generateCode("44348225996"), "Gobstoppers", 1.0D, 0.99D));
      grocery.add(new Item(Upc.generateCode("34323432343"), "Nerds", 2.0D, 1.44D));
      grocery.add(new Item(Upc.generateCode("54323432343"), "Doritos Club", 1.0D, 0.5D));
      grocery.add(new Item(Upc.generateCode("61519314159"), "Doritos", 1.0D, 1.25D));
      System.out.println(register.print(grocery));
      grocery.clear();
      grocery.add(new Item(Upc.generateCode("12345678901"), "Bananas", 1.0D, 1.5D));
      grocery.add(new Item(Upc.generateCode("22804918500"), "Beef", 0.5D, 5.75D));
      grocery.add(new Item(Upc.generateCode("64748119599"), "Chewing gum", 2.0D, 0.99D));
      grocery.add(new Item(Upc.generateCode("44348225996"), "Gobstoppers", 1.0D, 0.99D));
      System.out.println(register.print(grocery));
   }
}
