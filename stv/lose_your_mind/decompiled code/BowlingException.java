package stev.bowling;

public class BowlingException extends RuntimeException {
   private static final long serialVersionUID = 335042075617555432L;

   public BowlingException(String message) {
      super(message);
   }

   public BowlingException(Throwable t) {
      super(t);
   }
}
