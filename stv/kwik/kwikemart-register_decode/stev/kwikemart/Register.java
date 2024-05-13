package stev.kwikemart;

import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;

public final class Register {
   public static final float MAX_AMOUNT = 35.0F;
   private PaperRoll m_roll = null;
   private static final Register s_instance = new Register();
   private static final DecimalFormat s_cashFormatter = new DecimalFormat(" #0.00$;-#0.00$");
   private static final DecimalFormat s_quantityFormatter = new DecimalFormat("0.00");
   private static final SimpleDateFormat s_dateFormatter = new SimpleDateFormat("E MM/dd/yyyy hh:mm:ss");

   public static final Register getRegister() {
      return s_instance;
   }

   private Register() {
   }

   public final Register changePaper(PaperRoll r) {
      this.m_roll = r;
      return this;
   }

   public final String print(List<Item> list) throws StoreException {
      if (list.isEmpty()) {
         throw RegisterException.EmptyGroceryListException.instance;
      } else if (list.size() > 10) {
         throw RegisterException.TooManyItemsException.instance;
      } else {
         Set<Item> existing_upcs = new HashSet();
         float total = 0.0F;
         if (this.m_roll == null) {
            throw Register.NoPaperRollException.instance;
         } else {
            this.m_roll.println("------------------------------------------");
            this.m_roll.println("KWIK-E-MART SPRINGFIELD");
            this.m_roll.println(s_dateFormatter.format(new Date()));
            this.m_roll.println("");
            Iterator var5 = list.iterator();

            double line_price;
            while(var5.hasNext()) {
               Item item = (Item)var5.next();
               String upc = item.getUpc();
               line_price = item.getQuantity();
               this.checkUpc(item);
               if (line_price > 0.0D) {
                  if (existing_upcs.contains(item)) {
                     throw new Register.DuplicateItemException(upc, (Register.DuplicateItemException)null);
                  }

                  existing_upcs.add(item);
               }

               if (line_price < 0.0D) {
                  if (!existing_upcs.contains(item)) {
                     throw new Register.NoSuchItemException(upc, (Register.NoSuchItemException)null);
                  }

                  existing_upcs.remove(item);
               }

               this.checkQuantity(item);
               this.checkAmount(item);
               int category = Upc.getDigit(upc.substring(0, 1));
               String description = "";
               double line_price = item.getRetailPrice() * item.getQuantity();
               if (category == 2) {
                  description = pad(item.getDescription() + " " + formatQuantity(item.getQuantity()) + " @ " + formatPrice(item.getRetailPrice()), 20);
               } else {
                  description = pad(item.getDescription() + " x " + (int)item.getQuantity(), 20);
               }

               if (category != 5) {
                  total = (float)((double)total + line_price);
                  this.m_roll.println(item.getUpc() + " " + description + "  " + formatPrice(line_price));
               }
            }

            this.m_roll.println(pad("SUB-TOTAL", 33) + "  " + formatPrice((double)total));
            this.m_roll.println("");
            float tax = 0.05F * total;
            this.m_roll.println(pad("Tax SGST 5%", 33) + "  " + formatPrice((double)tax));
            total += tax;
            Iterator var15 = existing_upcs.iterator();

            while(var15.hasNext()) {
               Item item = (Item)var15.next();
               if (Upc.getDigit(item.getUpc().substring(0, 1)) == 5) {
                  if (item.getQuantity() != 1.0D) {
                     throw new CouponException.InvalidCouponQuantityException(item.getUpc());
                  }

                  line_price = item.getRetailPrice();
                  if ((double)total > line_price) {
                     total = (float)((double)total - line_price);
                     this.m_roll.println(item.getUpc() + " " + pad("Coupon: " + item.getDescription(), 20) + "  " + formatPrice(-line_price));
                  }
               }
            }

            if (list.size() > 4 && total > 2.0F) {
               this.m_roll.println(pad("Rebate for 5 items", 33) + "  " + formatPrice(-1.0D));
               --total;
            }

            this.m_roll.println(pad("TOTAL", 33) + "  " + formatPrice((double)total));
            this.m_roll.println("------------------------------------------");
            return this.m_roll.tearUp();
         }
      }
   }

   private void checkUpc(Item item) throws InvalidUpcException {
      String upc = item.getUpc();
      if (upc.isEmpty()) {
         throw new InvalidUpcException.NoUpcException(upc);
      } else if (upc.length() < 12) {
         throw new InvalidUpcException.UpcTooShortException(upc);
      } else if (upc.length() > 12) {
         throw new InvalidUpcException.UpcTooLongException(upc);
      } else {
         int i;
         int digit;
         for(i = 0; i < 11; ++i) {
            digit = Upc.getDigit(upc.substring(i, i + 1));
            if (digit < 0) {
               throw new InvalidUpcException.InvalidDigitException(upc, i);
            }
         }

         i = Upc.getCheckDigit(upc);
         digit = Upc.getDigit(upc.substring(11, 12));
         if (digit != i) {
            throw new InvalidUpcException.InvalidCheckDigitException(upc);
         }
      }
   }

   private void checkQuantity(Item item) throws InvalidQuantityException {
      String upc = item.getUpc();
      double q = item.getQuantity();
      int category = Upc.getDigit(upc.substring(0, 1));
      if (category != 2 && q % 1.0D != 0.0D) {
         throw new InvalidQuantityException.InvalidQuantityForCategoryException(upc);
      }
   }

   private void checkAmount(Item item) throws AmountException {
      String upc = item.getUpc();
      double a = item.getRetailPrice();
      if (a < 0.0D) {
         throw new AmountException.NegativeAmountException(upc);
      } else if (a > 35.0D) {
         throw new AmountException.AmountTooLargeException(upc);
      }
   }

   private static final String pad(String s, int width) {
      StringBuilder out = new StringBuilder();
      if (s.length() > width) {
         return s.substring(0, width);
      } else {
         out.append(s);

         for(int i = s.length(); i < width; ++i) {
            out.append(" ");
         }

         return out.toString();
      }
   }

   private static final String formatPrice(double price) {
      return s_cashFormatter.format(price);
   }

   private static final String formatQuantity(double q) {
      return s_quantityFormatter.format(q);
   }

   public static final class DuplicateItemException extends RegisterException {
      private static final long serialVersionUID = 1L;

      private DuplicateItemException(String upc) {
         super("Item " + upc + " is already in the list");
      }

      // $FF: synthetic method
      DuplicateItemException(String var1, Register.DuplicateItemException var2) {
         this(var1);
      }
   }

   public static final class NoPaperRollException extends RegisterException {
      private static final long serialVersionUID = 1L;
      public static final Register.NoPaperRollException instance = new Register.NoPaperRollException();

      private NoPaperRollException() {
         super("There is no paper roll in the register");
      }
   }

   public static final class NoSuchItemException extends RegisterException {
      private static final long serialVersionUID = 1L;

      private NoSuchItemException(String upc) {
         super("Item " + upc + " is not already in the list");
      }

      // $FF: synthetic method
      NoSuchItemException(String var1, Register.NoSuchItemException var2) {
         this(var1);
      }
   }
}
