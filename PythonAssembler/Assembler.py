# Reads assembly program and produces machine code
# Usage: python Assembler.py [program].asm
# Output: [program].hack

class Parser:
  def __init__(self, input_file):
    self.command = ""
    self.idx = 0
    with open(input_file, 'r') as f:
      self.input_file = [x.strip().replace(" ","") for x in f.readlines()] # get rid of whitespace
      self.input_file = [x for x in self.input_file if x and x[0] != "/"] # get rid of newline and comment
  
  @staticmethod
  def strip(s):
    return s.replace(" ", "")
      
  def hasMoreCommands(self):
    return self.idx < len(self.input_file)
  
  def advance(self):
    if self.hasMoreCommands():
      self.command = self.input_file[self.idx]
      self.idx += 1
      
  def commandType(self):
    if self.command.startswith("@"):
      return "A"
    elif self.command.startswith("("):
      return "L"
    else:
      return "C"
    
  def symbol(self):
    if self.commandType() == "A":
      return self.command[1:]
    elif self.commandType() == "L":
      return self.command[1:-1]

  def dest(self):
    if "=" in self.command:
      return self.command.split("=")[0]
    else:
      return None

  def comp(self):
    if "=" in self.command: # can these both happen at the same time? ex. D=A+1;JGT
      return Parser.strip(self.command.split("=")[1])
    elif ";" in self.command:
      return Parser.strip(self.command.split(";")[0])
    else:
      return None
      
  def jump(self):
    if ";" in self.command:
      return self.command.split(";")[1].strip()
    else:
      return None
    
class Code:
  @staticmethod
  def dest(m):
    dest = {
    None: "000", "M": "001", "D": "010", "A": "100", "MD": "011", "AM": "101", "AD": "110", "AMD": "111"
    }
    return dest[m]

  @staticmethod
  def comp(m):
    comp = {
    None: "0000000", "0": "0101010","1": "0111111","-1": "0111010","D": "0001100","A": "0110000","!D": "0001101", "!A": "0110001", "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111", "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011", "A-D": "0000111", "D&A": "0000000", "D|A": "0010101", "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111", "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111", "D&M": "1000000", "D|M": "1010101"
    }
    return comp[m]
  
  @staticmethod
  def jump(m):
    jump = {
    None: "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
    }
    return jump[m]

if __name__ == "__main__":

  import sys

  assert len(sys.argv) == 2, "Usage: python Assembler.py [program].asm"
  print("Assembling " + sys.argv[1])
  input_file = sys.argv[1]
  output_file = open(input_file.replace(".asm", ".hack"), 'w')

  parser = Parser(input_file)
  print(parser.input_file)
  
  while parser.hasMoreCommands():
    parser.advance()
    
    print(parser.command)
    print(parser.commandType())
    print(parser.symbol())

    if parser.commandType() == "A": # do L and symbols later
      address = parser.symbol()
      output_file.write("0" + bin(int(address))[2:].zfill(15) + "\n") # get rid of 0b and pad with 0s
    elif parser.commandType() == "C":
      comp = Code.comp(parser.comp())
      dest = Code.dest(parser.dest())
      jump = Code.jump(parser.jump())
      output_file.write("111" + comp + dest + jump + "\n")
    
  output_file.close()