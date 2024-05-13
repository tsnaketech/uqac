package stev.kwikemart;

public abstract class RegisterException extends StoreException {
   private static final long serialVersionUID = 1L;

   public RegisterException(String message) {
      super(message);
   }

   public static final class EmptyGroceryListException extends RegisterException {
      private static final long serialVersionUID = 1L;
      public static final RegisterException.EmptyGroceryListException instance = new RegisterException.EmptyGroceryListException();

      private EmptyGroceryListException() {
         super("The grocery list is empty");
      }
   }

   public static final class TooManyItemsException extends RegisterException {
      private static final long serialVersionUID = 1L;
      public static final RegisterException.TooManyItemsException instance = new RegisterException.TooManyItemsException();

      private TooManyItemsException() {
         super("Too many items in the grocery list");
      }
   }
}
